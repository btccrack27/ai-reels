-- AI Reels Generator - Supabase Schema
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'free',
    stripe_customer_id TEXT,
    subscription_id UUID,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Subscriptions Table
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    plan TEXT NOT NULL CHECK (plan IN ('free', 'basic', 'pro', 'enterprise')),
    status TEXT NOT NULL CHECK (status IN ('active', 'canceled', 'past_due', 'trialing')),
    stripe_subscription_id TEXT UNIQUE,
    current_period_start TIMESTAMPTZ NOT NULL,
    current_period_end TIMESTAMPTZ NOT NULL,
    cancel_at_period_end BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Contents Table (polymorphic)
CREATE TABLE IF NOT EXISTS contents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('hook', 'script', 'shotlist', 'voiceover', 'caption', 'broll', 'calendar')),
    status TEXT NOT NULL DEFAULT 'completed' CHECK (status IN ('generating', 'completed', 'failed')),
    data JSONB NOT NULL,
    prompt TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Usage Tracking Table
CREATE TABLE IF NOT EXISTS usage_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    content_type TEXT NOT NULL,
    count INTEGER DEFAULT 0,
    period_start TIMESTAMPTZ NOT NULL,
    period_end TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, content_type, period_start, period_end)
);

-- Indexes für Performance
CREATE INDEX idx_contents_user_id ON contents(user_id);
CREATE INDEX idx_contents_type ON contents(type);
CREATE INDEX idx_contents_created_at ON contents(created_at DESC);
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_id ON subscriptions(stripe_subscription_id);
CREATE INDEX idx_usage_user_content ON usage_tracking(user_id, content_type);
CREATE INDEX idx_usage_period ON usage_tracking(period_start, period_end);

-- Row Level Security (RLS) Policies

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE contents ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_tracking ENABLE ROW LEVEL SECURITY;

-- Users Policies
CREATE POLICY "Users can view own data"
    ON users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own data"
    ON users FOR UPDATE
    USING (auth.uid() = id);

-- Subscriptions Policies
CREATE POLICY "Users can view own subscription"
    ON subscriptions FOR SELECT
    USING (auth.uid() = user_id);

-- Contents Policies
CREATE POLICY "Users can view own contents"
    ON contents FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own contents"
    ON contents FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own contents"
    ON contents FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own contents"
    ON contents FOR DELETE
    USING (auth.uid() = user_id);

-- Usage Tracking Policies
CREATE POLICY "Users can view own usage"
    ON usage_tracking FOR SELECT
    USING (auth.uid() = user_id);

-- Functions

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contents_updated_at
    BEFORE UPDATE ON contents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_usage_updated_at
    BEFORE UPDATE ON usage_tracking
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Default Free Subscription Function
CREATE OR REPLACE FUNCTION create_default_subscription()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO subscriptions (
        user_id,
        plan,
        status,
        current_period_start,
        current_period_end
    ) VALUES (
        NEW.id,
        'free',
        'active',
        NOW(),
        NOW() + INTERVAL '1 month'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to create free subscription on user registration
CREATE TRIGGER create_user_subscription
    AFTER INSERT ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_default_subscription();

-- Comments
COMMENT ON TABLE users IS 'Registered users of the AI Reels Generator';
COMMENT ON TABLE subscriptions IS 'User subscription plans and status';
COMMENT ON TABLE contents IS 'Generated content (hooks, scripts, etc.) - polymorphic design';
COMMENT ON TABLE usage_tracking IS 'Tracks usage for rate limiting per subscription plan';

COMMENT ON COLUMN contents.data IS 'JSONB field containing type-specific content data';
COMMENT ON COLUMN contents.type IS 'Type of content: hook, script, shotlist, voiceover, caption, broll, calendar';
COMMENT ON COLUMN usage_tracking.count IS 'Number of generations in the current period';
