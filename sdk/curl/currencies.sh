#!/usr/bin/env bash
# Miau Finance — Multi-Currency API examples
# Usage: ./sdk/curl/currencies.sh
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

echo "=== Multi-Currency ==="
echo ""

echo "--- List supported currencies ---"
curl -s "$BASE/api/v1/currencies" -H "$AUTH_HEADER" | jq .

echo "--- Convert 100 USD to EUR ---"
curl -s "$BASE/api/v1/currencies/convert?from=USD&to=EUR&amount=100" \
  -H "$AUTH_HEADER" | jq .

echo "--- Live FX rates (USD base) ---"
curl -s "$BASE/api/v1/market/forex?base=USD" -H "$AUTH_HEADER" | jq .

echo "--- Global market overview ---"
curl -s "$BASE/api/v1/markets/global" -H "$AUTH_HEADER" | jq .
