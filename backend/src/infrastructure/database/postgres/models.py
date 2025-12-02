from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from .config import Base


class UserModel(Base):
    """SQLAlchemy Model für Users Tabelle"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(Text, unique=True, nullable=False, index=True)
    name = Column(Text, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, nullable=False, default='free')
    stripe_customer_id = Column(Text, nullable=True)
    subscription_id = Column(UUID(as_uuid=True), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SubscriptionModel(Base):
    """SQLAlchemy Model für Subscriptions Tabelle"""
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    plan = Column(
        Text,
        nullable=False,
        server_default='free'
    )
    status = Column(
        Text,
        nullable=False,
        server_default='active'
    )
    stripe_subscription_id = Column(Text, unique=True, nullable=True)
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("plan IN ('free', 'basic', 'pro', 'enterprise')", name='subscriptions_plan_check'),
        CheckConstraint("status IN ('active', 'canceled', 'past_due', 'trialing')", name='subscriptions_status_check'),
    )


class ContentModel(Base):
    """SQLAlchemy Model für Contents Tabelle (polymorphisch)"""
    __tablename__ = "contents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    type = Column(Text, nullable=False, index=True)
    status = Column(Text, nullable=False, default='completed')
    data = Column(JSONB, nullable=False)
    prompt = Column(Text, nullable=False)
    version = Column(Integer, default=1)
    metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "type IN ('hook', 'script', 'shotlist', 'voiceover', 'caption', 'broll', 'calendar')",
            name='contents_type_check'
        ),
        CheckConstraint(
            "status IN ('generating', 'completed', 'failed')",
            name='contents_status_check'
        ),
    )


class UsageTrackingModel(Base):
    """SQLAlchemy Model für Usage Tracking Tabelle"""
    __tablename__ = "usage_tracking"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    content_type = Column(Text, nullable=False)
    count = Column(Integer, default=0)
    period_start = Column(DateTime(timezone=True), nullable=False, index=True)
    period_end = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
