#!/usr/bin/env bash
# Portfolio & Analytics API examples
# Usage: bash portfolio.sh
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

echo "=== List Portfolios ==="
curl -s "$BASE/api/v1/portfolios" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Portfolio Summary ==="
curl -s "$BASE/api/v1/analytics/summary" -H "$AUTH_HEADER" | jq .

echo -e "\n=== PnL Timeseries ==="
curl -s "$BASE/api/v1/analytics/pnl/timeseries" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Comprehensive Risk ==="
curl -s "$BASE/api/v1/risk/comprehensive?ticker=AAPL" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Rolling Risk ==="
curl -s "$BASE/api/v1/risk/rolling?ticker=AAPL&benchmark=SPY" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Scenario Analysis ==="
curl -s "$BASE/api/v1/analytics/scenario/AAPL?scenario=bear" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Dividends ==="
curl -s "$BASE/api/v1/dividends/AAPL" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Dividend Calendar ==="
curl -s "$BASE/api/v1/dividends/calendar?tickers=AAPL,MSFT,JNJ" -H "$AUTH_HEADER" | jq .
