#!/usr/bin/env bash
# Market data API examples
# Usage: bash market.sh
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

echo "=== Live Prices ==="
curl -s "$BASE/api/v1/market/live?tickers=AAPL,MSFT,GOOGL" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Historical Data ==="
curl -s "$BASE/api/v1/market/historical/AAPL?period=6mo" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Market Movers ==="
curl -s "$BASE/api/v1/market/movers" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Sector Performance ==="
curl -s "$BASE/api/v1/market/sectors" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Market Indicators ==="
curl -s "$BASE/api/v1/market/indicators" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Forex Rates ==="
curl -s "$BASE/api/v1/market/forex?base=USD" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Crypto Prices ==="
curl -s "$BASE/api/v1/market/crypto?coin=bitcoin" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Global Markets ==="
curl -s "$BASE/api/v1/markets/global" -H "$AUTH_HEADER" | jq .
