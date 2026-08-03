#!/bin/bash
# 🐱 Miau Finance — Stripe Setup Script
# Run this after creating your Stripe account to go-live with billing.
# 
# Prerequisites:
#   1. Create a Stripe account: https://dashboard.stripe.com/register
#   2. Get your secret key: https://dashboard.stripe.com/apikeys
#   3. Get your webhook secret (optional for now, needed for recurring billing)
#
# Usage:
#   bash scripts/setup-stripe.sh

set -e

ENV_FILE="/home/jevgeniz/Projekte/miau-finance/.env"

echo "🐱 Miau Finance — Stripe Setup"
echo "════════════════════════════════"
echo ""

# Check if Stripe key already set
EXISTING_KEY=$(grep STRIPE_SECRET_KEY "$ENV_FILE" 2>/dev/null | grep -v "^#" | cut -d= -f2)
if [ -n "$EXISTING_KEY" ] && [ "$EXISTING_KEY" != "sk_live_..." ]; then
  echo "✅ Stripe key already configured"
  echo "  Current: ${EXISTING_KEY:0:12}..."
else
  echo "📝 Stripe is NOT configured — using DEV MODE (no real payments)"
  echo ""
  echo "To enable real payments:"
  echo "  1. Go to https://dashboard.stripe.com/register"
  echo "  2. Get your secret key (sk_live_...)"
  echo "  3. Run: nano $ENV_FILE"
  echo "     Add: STRIPE_SECRET_KEY=sk_live_your_key_here"
  echo ""
  echo "💡 Dev mode is active — users can test checkout without paying."
  echo "   Subscriptions are activated instantly in the database."
  echo "   Perfect for testing! Real payments work when you add keys."
fi

echo ""
echo "════════════════════════════════"
echo "📊  CURRENT BILLING STATUS"
echo "────────────────────────────────"

# Check dev mode checkout endpoint
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/token \
  -H 'Content-Type: application/json' \
     -d '{"username":"your_username","password":"your_password"}' 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
  echo "✅ Backend authenticated"
  
  # Test dev mode checkout
  CHECKOUT=$(curl -s -X POST http://localhost:8000/api/v1/billing/checkout \
    -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' \
    -d '{"tier":"pro","success_url":"http://localhost:5173/billing/success","cancel_url":"http://localhost:5173/pricing"}' 2>/dev/null)
  
  if echo "$CHECKOUT" | grep -q "dev_mode"; then
    echo "✅ Dev mode checkout — working (no Stripe needed)"
    echo "   Try it: type 'pricing' in the terminal → click Subscribe"
  elif echo "$CHECKOUT" | grep -q "session_url"; then
    echo "✅ Live mode checkout — working (Stripe connected)"
  else
    echo "⚠️  Checkout returned: $CHECKOUT"
  fi
  
  # Check current subscription
  SUB=$(curl -s http://localhost:8000/api/v1/billing/subscription \
    -H "Authorization: Bearer $TOKEN" 2>/dev/null)
  TIER=$(echo "$SUB" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tier','unknown'))" 2>/dev/null)
  echo "✅ Current tier: $TIER"
else
  echo "❌ Backend not reachable — start services first"
fi

echo ""
echo "════════════════════════════════"
echo "📋  PRICING (EUR)"
echo "────────────────────────────────"
echo "  Free        €0/mo     — Basic access"
echo "  Pro         €99/mo    — Full trading + AI advisor"
echo "  Enterprise  €396/mo   — Unlimited + dedicated support"
echo ""
echo "  🔧 To change prices, edit backend/app/api/billing.py"
echo "  🎨 To change the UI, edit frontend/src/components/PricingPage.tsx"
echo ""
echo "════════════════════════════════"
echo "🚀  NEXT STEPS TO START EARNING"
echo "────────────────────────────────"
echo "  1. Create Stripe account (5 min): https://dashboard.stripe.com/register"
echo "  2. Add STRIPE_SECRET_KEY to .env"
echo "  3. Create products in Stripe dashboard (€99/mo Pro, €396/mo Enterprise)"
echo "  4. Add price IDs to .env: STRIPE_PRO_PRICE_ID, STRIPE_ENTERPRISE_PRICE_ID"
echo "  5. Restart backend: docker compose restart backend"
echo ""
echo "  OR: Keep using dev mode — test checkout without real payments"
echo "     (Subscriptions activate instantly — perfect for demos)"
echo ""
echo "🐱 The cat believes in you. Go make that EUR."
