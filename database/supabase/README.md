# Supabase Setup

## 1. Supabase Projekt erstellen

1. Gehe zu https://supabase.com
2. Erstelle ein neues Projekt
3. Notiere dir:
   - Project URL
   - `anon` public key
   - `service_role` secret key

## 2. Datenbank-Schema erstellen

1. Öffne den SQL Editor in Supabase
2. Kopiere den Inhalt von `schema.sql`
3. Führe das SQL-Script aus

Das Schema erstellt:
- `users` Tabelle
- `subscriptions` Tabelle
- `contents` Tabelle (polymorphisch für alle Content-Typen)
- `usage_tracking` Tabelle
- Alle notwendigen Indexes
- Row Level Security (RLS) Policies
- Triggers für `updated_at` Felder
- Auto-Erstellung von FREE Subscriptions für neue User

## 3. Environment Variables setzen

Backend `.env`:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

Frontend `.env.local`:
```
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## 4. Testen

Teste die Verbindung mit:
```bash
cd backend
python -c "from supabase import create_client; client = create_client('YOUR_URL', 'YOUR_KEY'); print('Connected!')"
```

## Datenbank-Struktur

### Users
- Speichert registrierte User
- Automatische FREE Subscription bei Registration

### Subscriptions
- Verwaltet Plan (FREE, BASIC, PRO, ENTERPRISE)
- Stripe Integration via `stripe_subscription_id`
- Period-Tracking für monatliche Limits

### Contents
- Polymorphisches Design: alle 7 Content-Typen in einer Tabelle
- `data` JSONB-Feld enthält typ-spezifische Daten
- Versionierung via `version` Feld

### Usage Tracking
- Trackt Generierungen pro Content-Typ
- Monatliche Periods für Rate-Limiting
- Automatischer Reset am Perioden-Ende
