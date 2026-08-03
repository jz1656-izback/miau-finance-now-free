#!/bin/bash
# 🐱💸 MIAU FINANCE GO-LIVE SCRIPT
# Run this after you have your Stripe keys and ngrok token
# This script configures everything needed to start accepting payments

BOLD='\033[1m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; RED='\033[0;31m'; NC='\033[0m'

echo -e "${CYAN}${BOLD}"
echo '  ╱|、'
echo ' (˚ˎ 。7     MIAU FINANCE GO-LIVE LAUNCHER'
echo '  |、˜〵      "Let the cat take your payments."'
echo '  じしˍ,)ノ'
echo -e "${NC}"

# ── Step 1: Check .env for Stripe keys ──
echo -e "\n${BOLD}💳 STEP 1: Stripe Keys${NC}"
if grep -q "sk_live_" .env 2>/dev/null; then
  echo -e "  ${GREEN}✅ Stripe live keys found${NC}"
elif grep -q "sk_test_" .env 2>/dev/null; then
  echo -e "  ${YELLOW}⚠️  Test keys found (no real charges)${NC}"
else
  echo -e "  ${RED}❌ No Stripe keys in .env${NC}"
  echo -e "  📝 Add your keys:"
  echo -e "     STRIPE_SECRET_KEY=sk_live_xxx"
  echo -e "     STRIPE_PUBLISHABLE_KEY=pk_live_xxx"
  echo -e "     STRIPE_WEBHOOK_SECRET=whsec_xxx"
  echo -e "     STRIPE_PRO_PRICE_ID=price_xxx"
  echo -e "     STRIPE_ENTERPRISE_PRICE_ID=price_xxx"
  echo ""
  echo -e "  🔗 https://dashboard.stripe.com/apikeys"
  echo -e "  🔗 https://dashboard.stripe.com/products"
fi

# ── Step 2: Verify registration endpoint ──
echo -e "\n${BOLD}🔐 STEP 2: Registration Endpoint${NC}"
REGISTRATION_TEST=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"golive_test_'$(date +%s)'","email":"golive@test.com","password":"test123"}' 2>/dev/null)
if [ "$REGISTRATION_TEST" = "201" ]; then
  echo -e "  ${GREEN}✅ Registration works${NC}"
else
  echo -e "  ${RED}❌ Registration returned $REGISTRATION_TEST${NC}"
  echo -e "  Try: docker compose restart backend"
fi

# ── Step 3: Test checkout endpoint ──
echo -e "\n${BOLD}💶 STEP 3: Billing Checkout${NC}"
CHECKOUT_TEST=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/v1/billing/checkout \
  -H "Content-Type: application/json" \
  -d '{"tier":"pro"}' 2>/dev/null)
if [ "$CHECKOUT_TEST" = "200" ]; then
  echo -e "  ${GREEN}✅ Checkout endpoint responds${NC}"
elif [ "$CHECKOUT_TEST" = "401" ]; then
  echo -e "  ${YELLOW}⚠️  Checkout requires auth (login first)${NC}"
else
  echo -e "  ${YELLOW}⚠️  Checkout: $CHECKOUT_TEST (dev mode = OK)${NC}"
fi

# ── Step 4: Check ngrok ──
echo -e "\n${BOLD}🌐 STEP 4: Public URL${NC}"
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['tunnels'][0]['public_url'])" 2>/dev/null)
if [ -n "$NGROK_URL" ]; then
  echo -e "  ${GREEN}✅ ngrok tunnel active: ${CYAN}$NGROK_URL${NC}"
  echo -e "  📝 Share this URL: ${CYAN}$NGROK_URL${NC}"
else
  echo -e "  ${YELLOW}⚠️  No ngrok tunnel running${NC}"
  echo -e "  Install: sudo apt install ngrok"
  echo -e "  Auth:    ngrok authtoken YOUR_TOKEN"
  echo -e "  Start:   ngrok http 5173"
  echo -e "  🔗 https://dashboard.ngrok.com/get-started/your-authtoken"
fi

# ── Step 5: Startup services ──
echo -e "\n${BOLD}🐳 STEP 5: Services Status${NC}"
for p in 5173 5174 5175 5176 5177 5178 5179 5181 8000; do
  code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$p/ --connect-timeout 1 2>/dev/null)
  if [ "$code" = "200" ] || [ "$code" = "404" ]; then
    echo -e "  ${GREEN}✅ :$p → $code${NC}"
  else
    echo -e "  ${RED}❌ :$p → $code${NC}"
  fi
done

# ── Summary ──
echo -e "\n${CYAN}${BOLD}"
echo '  ╔══════════════════════════════════════════╗'
echo '  ║     GO-LIVE CHECKLIST                    ║'
echo '  ╚══════════════════════════════════════════╝'
echo -e "${NC}"
echo "  [ ] ngrok URL shared with the world"
echo "  [ ] Stripe live keys in .env"
echo "  [ ] Stripe products created (€99 Pro, €396 Enterprise)"
echo "  [ ] Test payment goes through"
echo "  [ ] Revenue tracking shows your 20%"
echo "  [ ] Post on Reddit, Twitter, LinkedIn"
echo ""
echo -e "${YELLOW}  After first payment: type 'revenue' in the terminal${NC}"
echo -e "${YELLOW}  Your 20%: type 'revenue payout'${NC}"
echo ""
