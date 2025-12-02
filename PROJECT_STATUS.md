# AI Reels Generator - Project Status

**Stand:** 01.12.2024
**GitHub:** https://github.com/btccrack27/ai-reels
**Vercel:** https://frontend-christians-projects-3af5506a.vercel.app

---

## 🎯 Projekt-Übersicht

Ein SaaS für Instagram Reels Content-Generierung mit AI:
- 7 Content-Typen (Hooks, Scripts, Shotlists, Voiceover, Captions, B-Roll, Calendar)
- Claude 3.5 Sonnet für Content-Generierung
- Vercel Postgres Datenbank
- Stripe Subscriptions (in Arbeit)
- PDF Export für alle Content-Typen

**Tech Stack:**
- Frontend: Next.js 14 + TypeScript + Tailwind
- Backend: Python FastAPI + SQLAlchemy
- AI: Anthropic Claude 3.5 Sonnet
- Database: Vercel Postgres (Neon)
- Storage: Vercel Blob
- Architecture: Clean Architecture

---

## ✅ Was ist fertig (75%)

### Phase 1: Domain Layer (100%)

**Domain Entities** (`backend/src/domain/entities/`)
- ✅ `content.py` - Basis-Entity (ContentType, ContentStatus)
- ✅ `hook.py` - 10 Hooks (5-10 Wörter)
- ✅ `script.py` - 2-4 Szenen Script (10-20 Sek)
- ✅ `shotlist.py` - 3-4 Shot Beschreibungen
- ✅ `voiceover.py` - 10-20 Sek Voiceover
- ✅ `caption.py` - Caption + 15 Hashtags
- ✅ `broll.py` - 10 B-Roll Ideen
- ✅ `calendar.py` - 30-Tage Content-Plan
- ✅ `user.py` - User mit Roles
- ✅ `subscription.py` - Subscription mit Plan-Limits
- ✅ `usage.py` - Usage-Tracking

**Domain Interfaces** (`backend/src/domain/interfaces/`)
- ✅ `content_repository.py` - IContentRepository
- ✅ `user_repository.py` - IUserRepository
- ✅ `subscription_repository.py` - ISubscriptionRepository
- ✅ `usage_repository.py` - IUsageRepository

**Domain Services** (`backend/src/domain/services/`)
- ✅ `rate_limiter.py` - Rate-Limiting pro Plan
- ✅ `content_validator.py` - Content-Validierung

### Phase 2: Infrastructure Layer (75%)

**Claude API** (`backend/src/infrastructure/ai_services/`)
- ✅ `claude_service.py` - 7 Generierungs-Methoden
  - `generate_hooks()` - 10 virale Hooks
  - `generate_script()` - Script mit Szenen
  - `generate_shotlist()` - 3-4 Shots
  - `generate_voiceover()` - Voiceover Text
  - `generate_caption()` - Caption + Hashtags
  - `generate_broll_ideas()` - 10 B-Roll Ideen
  - `generate_calendar()` - 30-Tage Plan
- ✅ `claude_prompts.py` - Optimierte Prompt-Templates

**Vercel Postgres** (`backend/src/infrastructure/database/postgres/`)
- ✅ `config.py` - Async DB Config (asyncpg)
- ✅ `models.py` - SQLAlchemy Models (4 Tabellen)
- ✅ `content_repository.py` - Content CRUD
- ✅ `user_repository.py` - User CRUD
- ✅ `subscription_repository.py` - Subscription CRUD
- ✅ `usage_repository.py` - Usage Tracking

**PDF Generator** (`backend/src/infrastructure/pdf/`)
- ✅ `pdf_generator.py` - 7 Export-Methoden
  - ReportLab-basiert
  - Branded PDFs mit custom Styling
  - A4 Format, professionelles Layout

**Noch fehlt:**
- ⏳ Stripe Integration

---

## 🗄️ Datenbank Schema (Vercel Postgres)

**4 Tabellen erstellt:**

### `users`
```sql
- id (UUID, PK)
- email (TEXT, UNIQUE)
- name (TEXT)
- password_hash (TEXT)
- role (TEXT) - free, basic, pro, enterprise
- stripe_customer_id (TEXT)
- subscription_id (UUID, FK)
- is_active (BOOLEAN)
- created_at, updated_at (TIMESTAMPTZ)
```

### `subscriptions`
```sql
- id (UUID, PK)
- user_id (UUID, FK → users)
- plan (TEXT) - free, basic, pro, enterprise
- status (TEXT) - active, canceled, past_due, trialing
- stripe_subscription_id (TEXT, UNIQUE)
- current_period_start, current_period_end (TIMESTAMPTZ)
- cancel_at_period_end (BOOLEAN)
- created_at, updated_at (TIMESTAMPTZ)
```

### `contents`
```sql
- id (UUID, PK)
- user_id (UUID, FK → users)
- type (TEXT) - hook, script, shotlist, voiceover, caption, broll, calendar
- status (TEXT) - generating, completed, failed
- data (JSONB) - Polymorphisch: typ-spezifische Daten
- prompt (TEXT) - Original User-Prompt
- version (INTEGER)
- metadata (JSONB)
- created_at, updated_at (TIMESTAMPTZ)
```

### `usage_tracking`
```sql
- id (UUID, PK)
- user_id (UUID, FK → users)
- content_type (TEXT)
- count (INTEGER)
- period_start, period_end (TIMESTAMPTZ)
- created_at, updated_at (TIMESTAMPTZ)
```

**Features:**
- UUID Primary Keys
- Indexes auf user_id, type, created_at
- Foreign Keys mit CASCADE
- Triggers für updated_at
- Auto-Erstellung von FREE Subscriptions

---

## 📊 Subscription Plans & Limits

### FREE Plan
- 5 Hooks / Monat
- 3 Scripts / Monat
- 3 Shotlists / Monat
- 3 Voiceovers / Monat
- 5 Captions / Monat
- 3 B-Roll Ideas / Monat
- 1 Calendar / Monat
- 2 PDF Exports / Monat

### BASIC Plan ($19/mo)
- 50 Hooks
- 30 Scripts
- 30 Shotlists
- 30 Voiceovers
- 50 Captions
- 30 B-Roll Ideas
- 5 Calendars
- 20 PDF Exports

### PRO Plan ($49/mo)
- 500 Hooks
- 300 Scripts
- 300 Shotlists
- 300 Voiceovers
- 500 Captions
- 300 B-Roll Ideas
- 20 Calendars
- 200 PDF Exports

### ENTERPRISE Plan ($199/mo)
- Unlimited alles

---

## 🏗️ Clean Architecture Struktur

```
Domain Layer (Geschäftslogik)
  ↓ depends on
Application Layer (Use Cases)
  ↓ depends on
Infrastructure Layer (Claude API, DB, PDF)
  ↓ depends on
Presentation Layer (FastAPI, Next.js)
```

**Vorteile:**
- ✅ Testbar: Jede Schicht isoliert testbar
- ✅ Austauschbar: Claude → andere AI, Postgres → MongoDB möglich
- ✅ Wartbar: Klare Verantwortlichkeiten
- ✅ Business-fokussiert: Domain-Logik unabhängig von Frameworks

---

## 📁 Wichtigste Dateien

### Backend Core
```
backend/src/
├── domain/
│   ├── entities/           # 11 Entities
│   ├── interfaces/         # 4 Interfaces
│   └── services/           # 2 Services
├── infrastructure/
│   ├── ai_services/
│   │   ├── claude_service.py       # ⭐ AI-Generierung
│   │   └── claude_prompts.py       # Prompt-Templates
│   ├── database/postgres/
│   │   ├── config.py               # DB-Config
│   │   ├── models.py               # SQLAlchemy Models
│   │   ├── content_repository.py   # ⭐ Content CRUD
│   │   ├── user_repository.py
│   │   ├── subscription_repository.py
│   │   └── usage_repository.py
│   └── pdf/
│       └── pdf_generator.py        # ⭐ PDF Export
└── main.py                          # FastAPI App
```

### Datenbank
```
database/
└── vercel-postgres/
    ├── schema.sql          # ⭐ DB Schema
    └── README.md           # Setup-Anleitung
```

### Frontend (Basis)
```
frontend/
├── src/
│   └── presentation/
│       └── pages/
│           └── app/
│               └── layout.tsx
├── package.json
├── tsconfig.json
└── vercel.json
```

---

## 🔧 Environment Variables

### Backend (.env)
```bash
# Vercel Postgres
DATABASE_URL=postgresql+asyncpg://...
POSTGRES_URL=postgres://...
POSTGRES_URL_NON_POOLING=postgres://...

# Claude AI
ANTHROPIC_API_KEY=sk-ant-...

# Vercel Blob
BLOB_READ_WRITE_TOKEN=vercel_blob_rw_...

# Stripe (noch nicht implementiert)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256

# App
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 Wie es funktioniert

### Content-Generierung Flow

```
1. User sendet Prompt
   ↓
2. Use Case prüft Rate-Limits (RateLimiter)
   ↓
3. Claude API generiert Content (ClaudeService)
   ↓
4. Content wird validiert (ContentValidator)
   ↓
5. In Datenbank gespeichert (ContentRepository)
   ↓
6. Usage-Counter erhöht (UsageRepository)
   ↓
7. Content zurück an User
```

### PDF Export Flow

```
1. User klickt "PDF Export"
   ↓
2. Use Case prüft PDF-Limit
   ↓
3. Content aus DB laden (ContentRepository)
   ↓
4. PDF generieren (PDFGenerator)
   ↓
5. Optional: Upload zu Vercel Blob
   ↓
6. PDF als Download/URL zurück
```

---

## 📦 Dependencies

### Backend (requirements.txt)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
sqlalchemy==2.0.25
asyncpg==0.29.0             # Vercel Postgres
anthropic==0.18.1           # Claude API
reportlab==4.1.0            # PDF Generation
stripe==8.2.0               # Stripe (vorbereitet)
PyJWT==2.8.0                # Authentication
passlib==1.7.4              # Password Hashing
bcrypt==4.1.2
redis==5.0.1
pytest==7.4.4
httpx==0.26.0
```

### Frontend (package.json)
```json
{
  "next": "^14.2.0",
  "react": "^18.3.0",
  "typescript": "^5.4.0",
  "tailwindcss": "^3.4.0",
  "axios": "^1.7.0",
  "zustand": "^4.5.0"
}
```

---

## 🧪 Was getestet werden kann

### Lokale Entwicklung

```bash
# Backend starten
cd backend
source .env
uvicorn src.main:app --reload

# Frontend starten
cd frontend
npm run dev

# Docker (komplettes Setup)
docker-compose up
```

### Claude API testen

```python
from infrastructure.ai_services.claude_service import ClaudeService

service = ClaudeService()
hooks = await service.generate_hooks("Fitness Motivation")
print(hooks.hooks)  # Liste von 10 Hooks
```

### Datenbank testen

```python
from infrastructure.database.postgres.config import async_session_maker
from infrastructure.database.postgres.content_repository import PostgresContentRepository

async with async_session_maker() as session:
    repo = PostgresContentRepository(session)
    contents = await repo.get_all(user_id="...")
```

### PDF testen

```python
from infrastructure.pdf.pdf_generator import PDFGenerator
from domain.entities.hook import HookContent

generator = PDFGenerator()
hooks = HookContent(hooks=["Hook 1", "Hook 2", ...])
pdf_bytes = generator.generate_hook_pdf(hooks, "Test Prompt")

with open("test.pdf", "wb") as f:
    f.write(pdf_bytes)
```

---

## ⏳ Was noch fehlt (25%)

### Phase 2 (restlich)
- ⏳ Stripe Integration
  - Checkout Sessions
  - Webhooks (subscription.created, invoice.paid)
  - Customer Portal
  - Plan Upgrades/Downgrades

### Phase 3: Application Layer
- ⏳ 7 Content-Generierungs Use Cases
- ⏳ Authentication Use Cases (Register, Login)
- ⏳ Subscription Management Use Cases
- ⏳ PDF Export Use Case
- ⏳ DTOs für alle Use Cases

### Phase 4: Presentation (API)
- ⏳ FastAPI Controllers (Content, Auth, Subscription, Export)
- ⏳ JWT Authentication Middleware
- ⏳ CORS Setup
- ⏳ Rate Limiting Middleware
- ⏳ Stripe Webhook Endpoint

### Phase 5-7: Frontend
- ⏳ Authentication Pages (Login, Register)
- ⏳ Generate Page mit 7 Content-Typen
- ⏳ Landing Page
- ⏳ Subscription Management Page
- ⏳ Content History Page
- ⏳ 7 Generator Components
- ⏳ 7 Display Components

---

## 📈 Nächste Schritte

### Kurzfristig (nächste Session)
1. **Stripe Integration** - Phase 2 abschließen
2. **Application Layer** - Use Cases erstellen
3. **API Controllers** - FastAPI Endpoints

### Mittelfristig
4. **Authentication** - JWT-basiert
5. **Frontend Core** - Generate Page + erste Generatoren
6. **Testing** - Unit & Integration Tests

### Langfristig
7. **Frontend Polish** - Alle 7 Generatoren
8. **Landing Page** - Marketing + Pricing
9. **Deployment** - Production-ready
10. **Monitoring** - Error Tracking & Analytics

---

## 🎯 Geschätzter Fortschritt

**Gesamt: ~30% Complete**

- ✅ Phase 1: Domain Layer (100%)
- ✅ Phase 2: Infrastructure (75%)
- ⏳ Phase 3: Application (0%)
- ⏳ Phase 4: API (0%)
- ⏳ Phase 5: Frontend Core (5%)
- ⏳ Phase 6: Frontend Generators (0%)
- ⏳ Phase 7: Landing + Polish (0%)
- ⏳ Phase 8: Testing & Deploy (0%)

**Realistische Timeline:**
- Phase 2 abschließen: 1-2 Stunden
- Phase 3-4: 3-4 Stunden
- Phase 5-7: 8-10 Stunden
- Phase 8: 2-3 Stunden

**Total: ~20 Stunden** bis Production-ready

---

## 💡 Highlights

### Was besonders gut ist:
- ✅ **Clean Architecture** - Professionelle Code-Struktur
- ✅ **Claude 3.5 Sonnet** - Beste AI für deutschen Content
- ✅ **Vercel Stack** - Modern, skalierbar, developer-friendly
- ✅ **PDF Export** - Professionelle, branded PDFs
- ✅ **Type-Safety** - Python Type Hints + TypeScript
- ✅ **Async/Await** - Performance-optimiert
- ✅ **Plan-Limits** - Durchdachtes Subscription-Modell

### Was unique ist:
- 🌟 7 spezialisierte Content-Typen (nicht nur "generic AI")
- 🌟 Deutsche Creator-Sprache (TikTok/Reel-optimiert)
- 🌟 Polymorphic Content Storage (flexibel erweiterbar)
- 🌟 Domain-driven Design (wartbar, testbar)

---

## 📞 Support

**GitHub:** https://github.com/btccrack27/ai-reels
**Commits:** 5 Commits, alle mit Clean Commit Messages
**Branches:** main (deployed to Vercel)

---

Erstellt am 01.12.2024 mit Claude Code
