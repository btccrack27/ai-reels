# 🎬 AI Reels Generator

> Generate viral Instagram Reels, TikToks, and YouTube Shorts content with AI

A complete SaaS application for content creators to generate professional social media content using Claude 3.5 Sonnet AI.

## 🚀 Features

### 7 AI-Powered Generators

1. **🎣 Hooks** - 10 viral attention-grabbing hooks (5-10 words each)
2. **📝 Scripts** - Complete 2-4 scene scripts with CTA (10-20 seconds)
3. **🎬 Shotlists** - Professional 3-4 shot descriptions with camera angles
4. **🎙️ Voiceovers** - 10-20 second voiceover text
5. **💬 Captions** - Engaging captions with 15 relevant hashtags
6. **🎥 B-Roll Ideas** - 10 creative B-Roll suggestions
7. **📅 Content Calendar** - 30-day content plan with daily themes and hooks

### Additional Features

- ✅ **PDF Export** - Download all generated content as professional PDFs
- ✅ **Content History** - Access all your generated content with search and filters
- ✅ **Usage Tracking** - Monitor your monthly usage across all tools
- ✅ **Subscription Management** - Flexible pricing plans with Stripe integration
- ✅ **Authentication** - Secure JWT-based authentication
- ✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile

## 🏗️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **AI**: Anthropic Claude 3.5 Sonnet
- **Database**: PostgreSQL (Vercel Postgres / Neon)
- **Payments**: Stripe
- **PDF Generation**: ReportLab
- **Architecture**: Clean Architecture (Domain, Application, Infrastructure, Presentation)

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

## 📦 Project Structure

```
ai-reels-generator/
├── backend/                 # FastAPI Backend
│   ├── src/
│   │   ├── domain/         # Entities, Interfaces, Services
│   │   ├── application/    # Use Cases, DTOs
│   │   ├── infrastructure/ # Databases, AI Services, PDF, Stripe
│   │   └── presentation/   # Controllers, Middlewares
│   ├── requirements.txt
│   └── .env.example
├── frontend/               # Next.js Frontend
│   ├── src/
│   │   ├── app/           # Pages (App Router)
│   │   ├── components/    # React Components
│   │   ├── lib/           # Utilities (API, Toast)
│   │   └── store/         # Zustand Stores
│   ├── package.json
│   └── .env.example
├── database/              # Database Schemas
│   └── vercel-postgres/
│       └── schema.sql
├── SETUP.md              # Complete setup guide
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (Vercel Postgres recommended)
- Anthropic Claude API key
- Stripe account

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ai-reels-generator.git
cd ai-reels-generator
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your credentials

# Start backend
uvicorn src.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install

# Copy and configure environment variables
cp .env.example .env.local
# Edit .env.local with your settings

# Start frontend
npm run dev
```

### 4. Database Setup

```bash
cd database/vercel-postgres
psql "YOUR_DATABASE_URL" < schema.sql
```

**See [SETUP.md](SETUP.md) for detailed setup instructions.**

## 💰 Pricing Plans

| Plan | Price | Hooks/month | Scripts/month | Calendars/month | PDFs/month |
|------|-------|-------------|---------------|-----------------|------------|
| **FREE** | €0 | 5 | 3 | 1 | 2 |
| **BASIC** | €19 | 50 | 30 | 5 | 20 |
| **PRO** | €49 | 500 | 300 | 20 | 200 |
| **ENTERPRISE** | €199 | ∞ | ∞ | ∞ | ∞ |

## 🎯 Use Cases

- **Content Creators**: Generate endless viral content ideas
- **Social Media Managers**: Plan and schedule 30 days of content
- **Marketing Agencies**: Create content for multiple clients
- **Influencers**: Stay consistent with daily posting
- **Small Businesses**: Professional content without hiring creators

## 📸 Screenshots

### Dashboard
Clean overview with stats, quick actions, and recent content.

### Generators
7 specialized tools for different content types with instant AI generation.

### Content History
Search, filter, and export all your generated content.

## 🔧 Development

### Run Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run test
```

### Build for Production

```bash
# Backend
cd backend
docker build -t ai-reels-backend .

# Frontend
cd frontend
npm run build
```

## 🚢 Deployment

### Recommended Stack

- **Backend**: Railway or Render
- **Frontend**: Vercel
- **Database**: Vercel Postgres
- **Blob Storage**: Vercel Blob (optional)

See [SETUP.md](SETUP.md) for deployment instructions.

## 📝 API Documentation

Once the backend is running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for Claude 3.5 Sonnet API
- **Stripe** for payment infrastructure
- **Vercel** for hosting and database
- **FastAPI** and **Next.js** communities

## 📧 Support

For support, email support@ai-reels-generator.com or open an issue.

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

Built with ❤️ using Claude Code
