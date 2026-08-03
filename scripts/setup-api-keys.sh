#!/bin/bash
# 🐱 Miau Finance — API Key Setup Helper
# Usage: bash scripts/setup-api-keys.sh
# This script helps you register for free API keys and configure them.

set -e

echo "🐱 Miau Finance — API Key Setup"
echo "════════════════════════════════"
echo ""

# Check if jq is available
if ! command -v jq &>/dev/null; then
  echo "⚠️  jq is recommended for JSON parsing. Install: sudo apt install jq"
fi

# Check backend
echo "🔍 Checking backend health..."
HEALTH=$(curl -s http://localhost:8000/api/v1/health 2>/dev/null)
if echo "$HEALTH" | grep -q "healthy"; then
  echo "✅ Backend is healthy"
else
  echo "❌ Backend is not responding. Start it first."
  exit 1
fi

# Get auth token — credentials from .env (V7-001/C1: no hardcoded credentials)
if [ -f .env ]; then
  AUTH_USER=$(grep -E '^DEMO_USERNAME=' .env | cut -d= -f2- | tr -d '"')
  AUTH_PASS=$(grep -E '^DEMO_PASSWORD=' .env | cut -d= -f2- | tr -d '"')
fi
AUTH_USER="${AUTH_USER:-$DEMO_USERNAME}"
AUTH_PASS="${AUTH_PASS:-$DEMO_PASSWORD}"
if [ -z "$AUTH_USER" ] || [ -z "$AUTH_PASS" ]; then
  echo "❌ DEMO_USERNAME/DEMO_PASSWORD not found. Set them in .env first."
  exit 1
fi
echo "🔑 Getting auth token..."
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/token \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$AUTH_USER\",\"password\":\"$AUTH_PASS\"}" 2>/dev/null | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "❌ Failed to get auth token"
  exit 1
fi
echo "✅ Authenticated"

# Check current keys
echo ""
echo "📋 Current key status:"
echo "────────────────────────"
curl -s "http://localhost:8000/api/v1/datavore/api-keys" \
  -H "Authorization: Bearer $TOKEN" 2>/dev/null | \
  python3 -c "
import sys,json
data = json.load(sys.stdin)
if 'keys' in data:
    for k in data['keys']:
        icon = '✅' if k.get('configured') else '❌'
        print(f\"  {icon} {k['provider']:15s} — {k['label']}\")
" 2>/dev/null

echo ""
echo "════════════════════════════════"
echo "📝  How to add API keys:"
echo ""
echo "  Option 1: Edit .env file"
echo "    nano /home/jevgeniz/Projekte/miau-finance/.env"
echo "    Then: docker compose restart backend"
echo ""
echo "  Option 2: Use the vault API (keys encrypted at rest)"
echo "    curl -X POST http://localhost:8000/api/v1/datavore/api-keys \\"
echo "      -H 'Authorization: Bearer $TOKEN' \\"
echo "      -H 'Content-Type: application/json' \\"
echo "      -d '{\"keys\": {\"finnhub_api_key\": \"your_key_here\"}}'"
echo ""
echo "  Option 3: Admin Dashboard at http://localhost:5179"
echo ""
echo "════════════════════════════════"
echo "🗝️  Free API Key Registration Links:"
echo "─────────────────────────────"
echo "  Finnhub      → https://finnhub.io/register"
echo "  Twelve Data  → https://twelvedata.com/"
echo "  BLS          → https://www.bls.gov/developers/"
echo "  EIA          → https://www.eia.gov/opendata/register.php"
echo "  FRED         → https://fred.stlouisfed.org/docs/api/api_key.html"
echo "  CoinPaprika  → https://coinpaprika.com/api/"
echo "  Etherscan    → https://etherscan.io/register"
echo "  News API     → https://newsapi.org/"
echo "  Alpha Vantage→ https://www.alphavantage.co/"
echo ""
