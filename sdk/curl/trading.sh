#!/usr/bin/env bash
# Trading & Orders API examples
# Usage: bash trading.sh
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

echo "=== List Orders ==="
curl -s "$BASE/api/v1/orders" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Paper Trading Portfolios ==="
curl -s "$BASE/api/v1/paper/portfolios" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Strategies ==="
curl -s "$BASE/api/v1/strategies" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Backtest Strategy ==="
curl -s "$BASE/api/v1/signals/backtest?ticker=AAPL&strategy=sma_cross" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Trading Signals ==="
curl -s "$BASE/api/v1/signals/generate?ticker=AAPL" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Multi-Signal ==="
curl -s "$BASE/api/v1/signals/multi?tickers=AAPL,MSFT,GOOGL" -H "$AUTH_HEADER" | jq .
