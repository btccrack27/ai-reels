# AI Reels Generator - Setup Guide

Complete setup guide for the AI Reels Generator SaaS application.

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL database (Vercel Postgres recommended)
- Anthropic Claude API key
- Stripe account

---

## 1. Database Setup (Vercel Postgres)

### Create Postgres Database

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Navigate to **Storage** > **Create Database**
3. Select **Postgres** (powered by Neon)
4. Name your database: `ai-reels-db`
5. Select region closest to your users

### Get Connection String

1. In Vercel Dashboard, go to your Postgres database
2. Copy the connection string from `.env.local` tab
3. Save it for later use

### Run Database Schema

```bash
cd database/vercel-postgres
psql "YOUR_CONNECTION_STRING_HERE" < schema.sql
```

Or use Vercel CLI:

```bash
vercel env pull .env.local
psql "$(grep POSTGRES_URL .env.local | cut -d '=' -f2-)" < schema.sql
```

---

## 2. Backend Setup

### Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```env
DATABASE_URL=postgresql://...  # From Vercel Postgres
ANTHROPIC_API_KEY=sk-ant-...   # From console.anthropic.com
STRIPE_SECRET_KEY=sk_test_...  # From dashboard.stripe.com
STRIPE_WEBHOOK_SECRET=whsec_... # From Stripe webhook setup
JWT_SECRET_KEY=...             # Generate with: openssl rand -hex 32
```

### Create Stripe Products

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/products)
2. Create 3 products:
   - **Basic**: €19/month
   - **Pro**: €49/month
   - **Enterprise**: €199/month
3. Copy the Price IDs (price_xxx) to your `.env`

### Start Backend

```bash
uvicorn src.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

---

## 3. Frontend Setup

### Install Dependencies

```bash
cd frontend
npm install
```

### Configure Environment Variables

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### Start Frontend

```bash
npm run dev
```

Frontend runs at: http://localhost:3000

---

## 4. Stripe Webhook Setup (Local Development)

### Install Stripe CLI

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Windows
scoop install stripe

# Linux
# See: https://stripe.com/docs/stripe-cli
```

### Login to Stripe

```bash
stripe login
```

### Forward Webhooks

```bash
stripe listen --forward-to localhost:8000/api/subscription/webhook
```

Copy the webhook signing secret (`whsec_...`) to your backend `.env`

---

## 5. Testing the Application

### Create Test User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "testpassword123"
  }'
```

### Login

1. Go to http://localhost:3000
2. Click "Login"
3. Use: test@example.com / testpassword123

### Test Content Generation

1. Go to **Generate** tab
2. Select "Hooks"
3. Enter a topic: "5 Tips for Better Sleep"
4. Click "10 Hooks generieren"

### Test Subscription

1. Go to **Subscription** tab
2. Click "Upgrade zu Basic"
3. Use Stripe test card: 4242 4242 4242 4242
4. Expiry: Any future date
5. CVC: Any 3 digits

---

## 6. Production Deployment

### Backend Deployment (Railway)

1. Create account at [Railway.app](https://railway.app)
2. Click **New Project** > **Deploy from GitHub**
3. Select your repository
4. Set root directory: `/backend`
5. Add environment variables from `.env`
6. Deploy

### Frontend Deployment (Vercel)

1. Push code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Click **Import Project**
4. Select your repository
5. Set root directory: `/frontend`
6. Add environment variables:
   - `NEXT_PUBLIC_API_URL`: Your Railway backend URL
   - `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Your Stripe key
7. Deploy

### Update Stripe Webhooks

1. Go to Stripe Dashboard > Webhooks
2. Add endpoint: `https://your-backend.railway.app/api/subscription/webhook`
3. Select events:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
4. Copy webhook secret to Railway environment variables

---

## 7. Environment Variables Reference

### Backend

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ |
| `ANTHROPIC_API_KEY` | Claude AI API key | ✅ |
| `STRIPE_SECRET_KEY` | Stripe secret key | ✅ |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret | ✅ |
| `STRIPE_PRICE_BASIC` | Price ID for Basic plan | ✅ |
| `STRIPE_PRICE_PRO` | Price ID for Pro plan | ✅ |
| `STRIPE_PRICE_ENTERPRISE` | Price ID for Enterprise plan | ✅ |
| `JWT_SECRET_KEY` | Secret for JWT tokens | ✅ |
| `CORS_ORIGINS` | Allowed CORS origins | ✅ |
| `FRONTEND_URL` | Frontend URL for redirects | ✅ |

### Frontend

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | ✅ |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | ✅ |

---

## 8. Troubleshooting

### Database Connection Error

- Verify `DATABASE_URL` in `.env`
- Check if database schema is created
- Ensure SSL mode is enabled for cloud databases

### Claude API Error

- Verify `ANTHROPIC_API_KEY` is correct
- Check API key has sufficient credits
- Ensure you're using Claude 3.5 Sonnet model

### Stripe Webhook Fails

- Verify `STRIPE_WEBHOOK_SECRET` matches Stripe dashboard
- Check webhook endpoint is publicly accessible
- Ensure correct events are selected in Stripe

### CORS Error

- Add frontend URL to `CORS_ORIGINS` in backend `.env`
- Restart backend server after changes
- Check browser console for specific error

---

## 9. Development Workflow

### Starting Development

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Stripe Webhooks (optional)
stripe listen --forward-to localhost:8000/api/subscription/webhook
```

### Making Changes

1. Make code changes
2. Both frontend and backend auto-reload
3. Test changes in browser
4. Commit to Git
5. Push to trigger deployment

---

## 10. Support

For issues or questions:
- Check logs in Railway/Vercel dashboards
- Review Stripe webhook logs
- Check Claude API usage
- Verify database connections

---

## Next Steps

- [ ] Set up production environment variables
- [ ] Configure custom domain
- [ ] Enable Vercel Analytics
- [ ] Set up error monitoring (Sentry)
- [ ] Configure email notifications
- [ ] Add backup strategy for database
