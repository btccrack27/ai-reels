# Vercel Postgres & Blob Setup

## Vercel Projekt

✅ **Projekt erstellt:** `ai-reels-generator`
🌐 **URL:** https://frontend-christians-projects-3af5506a.vercel.app
📦 **Project ID:** `prj_lRNp4wB2wfzVGBNztFjBuroREBWv`

---

## 1. Vercel Postgres hinzufügen

### Option A: Via Dashboard (Empfohlen)

1. Gehe zu https://vercel.com/dashboard
2. Öffne Projekt "frontend"
3. Gehe zu **Storage** Tab
4. Klicke **Create Database**
5. Wähle **Postgres**
6. Benenne die Datenbank: `ai-reels-generator-db`
7. Wähle Region: `Frankfurt (fra1)`
8. Klicke **Create**

### Option B: Via CLI

```bash
# Im Project Directory
cd /Users/christiansteffen/ai-reels-generator
vercel link
vercel postgres create ai-reels-generator-db
```

### Nach der Erstellung

Vercel erstellt automatisch diese Environment Variables:
```
POSTGRES_URL
POSTGRES_URL_NON_POOLING
POSTGRES_USER
POSTGRES_HOST
POSTGRES_PASSWORD
POSTGRES_DATABASE
```

---

## 2. Datenbank-Schema ausführen

### Via Vercel Dashboard

1. Gehe zu **Storage** → **Postgres** → Deine DB
2. Klicke auf **Query** Tab
3. Kopiere Inhalt von `schema.sql`
4. Führe das SQL aus

### Via CLI (mit psql)

```bash
# Connection String aus Vercel Dashboard kopieren
psql "postgres://user:pass@host/db" < database/vercel-postgres/schema.sql
```

### Via Code

```bash
cd backend
python scripts/init_db.py
```

---

## 3. Vercel Blob hinzufügen

### Via Dashboard

1. Gehe zu https://vercel.com/dashboard
2. Öffne Projekt "frontend"
3. Gehe zu **Storage** Tab
4. Klicke **Create** → **Blob**
5. Benenne den Store: `ai-reels-pdfs`
6. Klicke **Create**

Vercel erstellt automatisch:
```
BLOB_READ_WRITE_TOKEN
```

### Verwendung

Vercel Blob wird verwendet für:
- PDF Exports
- Zukünftig: Video/Audio Files
- Zukünftig: User Uploads

---

## 4. Environment Variables setzen

### Backend (.env)

```bash
# Vercel Postgres (automatisch gesetzt wenn deployed)
POSTGRES_URL="postgres://..."
POSTGRES_URL_NON_POOLING="postgres://..."

# Oder manuell für lokale Entwicklung
DATABASE_URL="postgresql://user:pass@host:5432/db"

# Anthropic Claude
ANTHROPIC_API_KEY="sk-ant-..."

# Stripe
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_WEBHOOK_SECRET="whsec_..."
STRIPE_BASIC_PRICE_ID="price_..."
STRIPE_PRO_PRICE_ID="price_..."
STRIPE_ENTERPRISE_PRICE_ID="price_..."

# JWT
JWT_SECRET_KEY="your-secret-key-here"
JWT_ALGORITHM="HS256"

# App
FRONTEND_URL="https://ai-reels-generator.vercel.app"

# Vercel Blob
BLOB_READ_WRITE_TOKEN="vercel_blob_rw_..."
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL="https://ai-reels-generator-api.vercel.app"
```

---

## 5. Lokale Entwicklung mit Vercel

### Postgres lokal nutzen

```bash
# Tunnel zu Vercel Postgres
vercel env pull .env

# Oder manuell Connection String aus Dashboard kopieren
# und in .env eintragen
```

### Development Server

```bash
# Frontend
cd frontend
vercel dev

# Backend (separat)
cd backend
uvicorn src.main:app --reload
```

---

## 6. Deployment

### Frontend deployen

```bash
cd frontend
vercel --prod
```

### Backend deployen

Vercel unterstützt Python nicht direkt. Optionen:

#### Option A: Railway/Render für Backend
```bash
# Backend auf Railway deployen
railway up
```

#### Option B: Vercel Serverless Functions
- Backend als API Routes in Next.js umschreiben
- Oder Python Runtime mit Vercel Functions

#### Option C: Docker auf Vercel (experimentell)
```bash
vercel --docker
```

**Empfehlung:** Railway oder Render für Python Backend, Vercel für Next.js Frontend

---

## 7. Datenbank-Verwaltung

### Via Vercel Dashboard

- SQL Query Editor
- Browse Data (Table View)
- Logs & Metrics

### Via psql (lokal)

```bash
# Connection String aus .env
psql $POSTGRES_URL

# Queries
\dt                    # List tables
\d users              # Describe users table
SELECT * FROM users;  # Query
```

### Via Python

```python
import asyncpg

conn = await asyncpg.connect(os.getenv('POSTGRES_URL'))
users = await conn.fetch('SELECT * FROM users')
```

---

## 8. Vercel Blob Verwendung

### Python (Backend)

```python
from vercel_blob import put, list

# PDF hochladen
blob = put('exports/reel-123.pdf', pdf_bytes, {
    'access': 'public',
    'content_type': 'application/pdf'
})
print(blob['url'])  # https://...vercel-storage.com/...pdf

# Liste aller Files
blobs = list()
```

### TypeScript (Frontend)

```typescript
import { put, list } from '@vercel/blob';

// Upload
const blob = await put('file.pdf', file, {
  access: 'public',
});
console.log(blob.url);

// List
const { blobs } = await list();
```

---

## Nächste Schritte

1. ✅ Vercel Projekt erstellt
2. ⏳ Postgres Database hinzufügen (Dashboard)
3. ⏳ Schema ausführen
4. ⏳ Blob Storage hinzufügen
5. ⏳ Environment Variables setzen
6. ⏳ Erste Deployment testen
