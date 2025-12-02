# Stripe Integration Setup

## Übersicht

AI Reels Generator nutzt Stripe für:
- **Subscriptions** - Monatliche Abrechnung (BASIC, PRO, ENTERPRISE)
- **Customer Portal** - Self-Service für User (Upgrade, Downgrade, Kündigung)
- **Webhooks** - Automatische Sync zwischen Stripe und unserer DB

---

## 1. Stripe Account Setup

### 1.1 Account erstellen

1. Gehe zu https://stripe.com
2. Erstelle Account (falls noch nicht vorhanden)
3. Aktiviere Test Mode (Toggle oben rechts)

### 1.2 API Keys holen

1. **Dashboard** → **Developers** → **API Keys**
2. Kopiere:
   - **Publishable key** (pk_test_...) → für Frontend
   - **Secret key** (sk_test_...) → für Backend

**Backend `.env`:**
```bash
STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY_HERE
```

**Frontend `.env.local`:**
```bash
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

---

## 2. Produkte & Preise erstellen

### 2.1 BASIC Plan ($19/Monat)

1. **Dashboard** → **Products** → **Add Product**
2. **Name:** `AI Reels Generator - BASIC`
3. **Description:** `50 Hooks, 30 Scripts, 30 Shotlists, 30 Voiceovers, 50 Captions, 30 B-Roll Ideas, 5 Calendars, 20 PDF Exports pro Monat`
4. **Pricing:**
   - **Price:** `$19.00 USD`
   - **Billing period:** `Monthly`
   - **Recurring:** Yes
5. **Save**
6. **Kopiere Price ID** (z.B. `price_1ABC2DEF3GHI4JKL`) → `.env`

### 2.2 PRO Plan ($49/Monat)

1. **Add Product**
2. **Name:** `AI Reels Generator - PRO`
3. **Description:** `500 Hooks, 300 Scripts, 300 Shotlists, 300 Voiceovers, 500 Captions, 300 B-Roll Ideas, 20 Calendars, 200 PDF Exports pro Monat`
4. **Pricing:** `$49.00 USD` / Monthly
5. **Save**
6. **Kopiere Price ID** → `.env`

### 2.3 ENTERPRISE Plan ($199/Monat)

1. **Add Product**
2. **Name:** `AI Reels Generator - ENTERPRISE`
3. **Description:** `Unlimited Content Generation & PDF Exports`
4. **Pricing:** `$199.00 USD` / Monthly
5. **Save**
6. **Kopiere Price ID** → `.env`

### 2.4 Environment Variables setzen

**Backend `.env`:**
```bash
STRIPE_BASIC_PRICE_ID=price_1ABC2DEF3GHI4JKL
STRIPE_PRO_PRICE_ID=price_1MNO5PQR6STU7VWX
STRIPE_ENTERPRISE_PRICE_ID=price_1YZA8BCD9EFG0HIJ
```

---

## 3. Webhooks konfigurieren

### 3.1 Webhook Endpoint erstellen

1. **Dashboard** → **Developers** → **Webhooks**
2. **Add endpoint**
3. **Endpoint URL:**
   - **Test Mode:** `https://your-backend.vercel.app/api/subscription/webhook`
   - **Local Testing:** `http://localhost:8000/api/subscription/webhook` (mit Stripe CLI)
4. **Events to send:**
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. **Add endpoint**

### 3.2 Webhook Secret kopieren

1. Klicke auf den erstellten Webhook
2. **Signing secret** → **Reveal**
3. Kopiere Secret (whsec_...)

**Backend `.env`:**
```bash
STRIPE_WEBHOOK_SECRET=whsec_ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX
```

---

## 4. Customer Portal aktivieren

Der Customer Portal erlaubt Usern:
- Zahlungsmethoden zu ändern
- Subscription zu upgraden/downgraden
- Subscription zu kündigen
- Rechnungen anzusehen

### 4.1 Portal konfigurieren

1. **Dashboard** → **Settings** → **Billing** → **Customer Portal**
2. **Activate test link** klicken
3. **Features aktivieren:**
   - ✅ Update payment method
   - ✅ Update subscription
   - ✅ Cancel subscription
   - ✅ Invoice history
4. **Cancellation behavior:**
   - **Option:** `Cancel at end of billing period` (empfohlen)
   - **Feedback:** Optional Survey aktivieren
5. **Save**

---

## 5. Lokale Entwicklung mit Stripe CLI

### 5.1 Stripe CLI installieren

**macOS:**
```bash
brew install stripe/stripe-cli/stripe
```

**Windows:**
```bash
scoop install stripe
```

**Linux:**
```bash
curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
sudo apt update
sudo apt install stripe
```

### 5.2 CLI authentifizieren

```bash
stripe login
```

Browser öffnet sich → Zugriff erlauben

### 5.3 Webhooks lokal forwarden

```bash
stripe listen --forward-to localhost:8000/api/subscription/webhook
```

Output:
```
Ready! Your webhook signing secret is whsec_... (^C to quit)
```

Kopiere das angezeigte Secret → `.env` (nur für lokale Entwicklung)

### 5.4 Test Webhooks triggern

```bash
# Subscription Created
stripe trigger customer.subscription.created

# Payment Succeeded
stripe trigger invoice.paid

# Payment Failed
stripe trigger invoice.payment_failed
```

---

## 6. Testing

### 6.1 Test Kreditkarten

Stripe bietet Test-Kreditkarten für verschiedene Szenarien:

**Erfolgreiche Zahlung:**
- **Nummer:** `4242 4242 4242 4242`
- **Datum:** Beliebiges zukünftiges Datum
- **CVC:** Beliebige 3 Ziffern
- **ZIP:** Beliebig

**Payment declined:**
- **Nummer:** `4000 0000 0000 0002`

**Requires authentication (3D Secure):**
- **Nummer:** `4000 0027 6000 3184`

Mehr Test-Karten: https://stripe.com/docs/testing#cards

### 6.2 Checkout Flow testen

1. **Frontend starten:**
   ```bash
   cd frontend && npm run dev
   ```

2. **Backend starten:**
   ```bash
   cd backend && uvicorn src.main:app --reload
   ```

3. **Stripe CLI forwarding starten:**
   ```bash
   stripe listen --forward-to localhost:8000/api/subscription/webhook
   ```

4. **Im Browser:**
   - Gehe zu `/subscription` Page
   - Klicke "Upgrade to BASIC"
   - Nutze Test-Kreditkarte `4242 4242 4242 4242`
   - Complete checkout

5. **Webhook prüfen:**
   - Im Stripe CLI sollte `customer.subscription.created` Event erscheinen
   - In der Datenbank sollte Subscription erstellt worden sein
   - User Role sollte von `free` auf `basic` geupdatet sein

---

## 7. Webhook Event Handling

Unsere Backend-Implementierung handled folgende Events:

### 7.1 `customer.subscription.created`

**Wann:** Neue Subscription wurde erstellt (nach erfolgreichem Checkout)

**Action:**
1. Subscription in DB erstellen
2. User Role updaten (free → basic/pro/enterprise)
3. Stripe Customer ID in User speichern

### 7.2 `customer.subscription.updated`

**Wann:** Subscription wurde geändert (Upgrade, Downgrade, Renewal)

**Action:**
1. Subscription Status updaten
2. Plan updaten (falls Upgrade/Downgrade)
3. Billing Period Dates updaten

### 7.3 `customer.subscription.deleted`

**Wann:** Subscription wurde gekündigt

**Action:**
1. Subscription Status → `canceled`
2. User Role → `free`
3. Usage Limits zurücksetzen

### 7.4 `invoice.paid`

**Wann:** Zahlung erfolgreich

**Action:**
1. Subscription Status → `active`
2. Current Period verlängern
3. Optional: Confirmation Email senden

### 7.5 `invoice.payment_failed`

**Wann:** Zahlung fehlgeschlagen

**Action:**
1. Subscription Status → `past_due`
2. Optional: Warning Email senden
3. Nach 3 Versuchen: Subscription kündigen

---

## 8. Production Deployment

### 8.1 Live Mode aktivieren

1. **Stripe Dashboard** → Toggle "Test Mode" → OFF
2. Neue API Keys holen:
   - **Live Secret Key** (sk_live_...)
   - **Live Publishable Key** (pk_live_...)

### 8.2 Live Produkte erstellen

1. Alle 3 Produkte (BASIC, PRO, ENTERPRISE) im Live Mode neu erstellen
2. Price IDs kopieren

### 8.3 Live Webhook erstellen

1. **Webhooks** → Live Mode
2. Endpoint: `https://your-production-backend.vercel.app/api/subscription/webhook`
3. Gleiche Events wie Test Mode
4. Webhook Secret kopieren

### 8.4 Environment Variables setzen

**Vercel Backend:**
```bash
vercel env add STRIPE_SECRET_KEY
# sk_live_... eingeben

vercel env add STRIPE_WEBHOOK_SECRET
# whsec_... (Live) eingeben

vercel env add STRIPE_BASIC_PRICE_ID
# price_... (Live) eingeben

vercel env add STRIPE_PRO_PRICE_ID
# price_... (Live) eingeben

vercel env add STRIPE_ENTERPRISE_PRICE_ID
# price_... (Live) eingeben
```

**Vercel Frontend:**
```bash
vercel env add NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
# pk_live_... eingeben
```

### 8.5 Webhook testen

```bash
# Test Event senden
curl -X POST https://your-backend.vercel.app/api/subscription/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

---

## 9. Monitoring & Debugging

### 9.1 Stripe Dashboard

**Dashboard** → **Developers** → **Webhooks** → [Dein Endpoint]

Hier siehst du:
- Alle gesendeten Events
- Response Status Codes
- Retry Attempts
- Error Messages

### 9.2 Backend Logs

**Vercel Logs:**
```bash
vercel logs --follow
```

Prüfe auf:
- Webhook Empfang
- Event Processing
- DB Updates
- Errors

### 9.3 Database Prüfung

```bash
# Connect to Vercel Postgres
psql $POSTGRES_URL

# Prüfe Subscriptions
SELECT
  u.email,
  s.plan,
  s.status,
  s.current_period_end
FROM subscriptions s
JOIN users u ON u.id = s.user_id
WHERE s.status = 'active';
```

---

## 10. Troubleshooting

### Problem: Webhook Events kommen nicht an

**Lösung:**
1. Prüfe Endpoint URL in Stripe Dashboard
2. Prüfe ob Backend läuft (`curl https://your-backend.vercel.app/health`)
3. Prüfe Webhook Secret korrekt in `.env`
4. Prüfe CORS Settings (Stripe IPs müssen allowed sein)

### Problem: "Invalid signature" Error

**Lösung:**
1. Webhook Secret falsch → neu kopieren
2. Test Mode / Live Mode mismatch
3. Body parsing vor Signature Verification → Raw body nutzen

### Problem: Subscription wird nicht erstellt

**Lösung:**
1. Prüfe Logs: `vercel logs`
2. Prüfe ob `customer.subscription.created` Event ankam
3. Prüfe Database Connection
4. Prüfe User existiert in DB

### Problem: User hat bezahlt aber Role noch `free`

**Lösung:**
1. Prüfe ob Webhook Event processed wurde
2. Manuell Subscription Status checken:
   ```bash
   stripe subscriptions list --customer cus_...
   ```
3. Event manuell re-senden via Stripe Dashboard

---

## 11. Best Practices

### 11.1 Idempotency

Webhooks können mehrfach gesendet werden → **Idempotent processing**:
- Prüfe ob Event bereits verarbeitet wurde
- Nutze `event.id` als Unique Key
- Upsert statt Insert

### 11.2 Retry Logic

- Stripe retried Webhooks bis zu 3 Tage
- Return 2xx Status Code nur wenn erfolgreich processed
- Bei Errors: 5xx returnen → Stripe retried automatisch

### 11.3 Security

- ✅ **IMMER** Webhook Signature verifizieren
- ✅ HTTPS für Production Webhooks
- ✅ Secret Keys niemals in Frontend
- ✅ Environment Variables nutzen, nicht hardcoden

### 11.4 Monitoring

- Set up Alerts für failed webhooks
- Log alle Subscription Changes
- Daily Sync zwischen Stripe und DB (optional)

---

## 12. Pricing Übersicht

| Plan | Preis | Hooks | Scripts | Calendars | PDFs |
|------|-------|-------|---------|-----------|------|
| **FREE** | $0 | 5 | 3 | 1 | 2 |
| **BASIC** | $19/mo | 50 | 30 | 5 | 20 |
| **PRO** | $49/mo | 500 | 300 | 20 | 200 |
| **ENTERPRISE** | $199/mo | ∞ | ∞ | ∞ | ∞ |

---

## Resources

- **Stripe Docs:** https://stripe.com/docs
- **Checkout Docs:** https://stripe.com/docs/payments/checkout
- **Webhooks Docs:** https://stripe.com/docs/webhooks
- **Customer Portal Docs:** https://stripe.com/docs/billing/subscriptions/integrating-customer-portal
- **Test Cards:** https://stripe.com/docs/testing#cards

---

Erstellt am 01.12.2024 für AI Reels Generator
