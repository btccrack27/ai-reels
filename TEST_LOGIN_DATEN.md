# Test Login Daten - AI Reels Generator

## Admin/Team Account

**Email:** `admin@aireel.com`
**Passwort:** `Admin123!`
**Rolle:** PRO
**Subscription Plan:** PRO
**Status:** Active
**Gültig bis:** 2026-01-01

### PRO Plan Limits:
- 500 Hooks/Monat
- 300 Scripts/Monat
- 20 Kalender/Monat
- 200 PDF Exports/Monat
- Alle Features freigeschaltet

---

## Test Kunden Account

**Email:** `kunde@test.com`
**Passwort:** `Kunde123!`
**Rolle:** BASIC
**Subscription Plan:** BASIC
**Status:** Active
**Gültig bis:** 2026-01-01

### BASIC Plan Limits:
- 50 Hooks/Monat
- 30 Scripts/Monat
- 5 Kalender/Monat
- 20 PDF Exports/Monat
- Basis-Features

---

## Weitere Test-Accounts erstellen

Um weitere Test-Accounts zu erstellen, kannst du folgendes SQL verwenden:

```sql
-- Passwort hashen mit Python:
python -c "import bcrypt; print(bcrypt.hashpw('DeinPasswort123!'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))"

-- User anlegen:
INSERT INTO users (id, email, name, password_hash, role, is_active)
VALUES (
  gen_random_uuid(),
  'email@example.com',
  'User Name',
  '$2b$12$...',  -- gehashtes Passwort hier einfügen
  'free',  -- free, basic, pro, enterprise
  true
);

-- Subscription anlegen:
INSERT INTO subscriptions (id, user_id, plan, status, current_period_start, current_period_end)
VALUES (
  gen_random_uuid(),
  (SELECT id FROM users WHERE email = 'email@example.com'),
  'free',  -- free, basic, pro, enterprise
  'active',
  NOW(),
  NOW() + INTERVAL '30 days'
);

-- User subscription_id updaten:
UPDATE users
SET subscription_id = (SELECT id FROM subscriptions WHERE user_id = users.id)
WHERE email = 'email@example.com';
```

---

## FREE Plan Limits (zum Testen)

Falls du noch einen FREE User brauchst:
- 5 Hooks/Monat
- 3 Scripts/Monat
- 1 Kalender/Monat
- 2 PDF Exports/Monat

---

## Login URL

**Development:** http://localhost:3001/login
**Production:** TBD (nach Deployment)

---

## Notizen

- Passwörter sind mit bcrypt gehasht (12 Salting Rounds)
- User IDs:
  - Admin: `a0000000-0000-0000-0000-000000000001`
  - Kunde: `a0000000-0000-0000-0000-000000000002`
- Subscriptions laufen bis 2026-01-01 (über 1 Jahr)
- Beide Accounts sind aktiv und sofort einsatzbereit

**WICHTIG:** Diese Passwörter sind nur für Testing! Für Production verwende sichere, zufällige Passwörter.
