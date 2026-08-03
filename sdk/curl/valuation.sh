#!/usr/bin/env bash
# Miau Finance — Investment Banking Valuation API examples
# Usage: ./sdk/curl/valuation.sh [ticker]
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

TICKER="${1:-AAPL}"

echo "=== Investment Banking Toolkits ==="
echo ""

echo "--- DCF Valuation ---"
curl -s "$BASE/api/v1/analytics/valuation/dcf/$TICKER?growth=0.05&terminal_growth=0.025&years=5" \
  -H "$AUTH_HEADER" | jq .

echo "--- WACC Calculation ---"
curl -s "$BASE/api/v1/analytics/valuation/wacc/$TICKER" -H "$AUTH_HEADER" | jq .

echo "--- Comparable Company Analysis ---"
curl -s "$BASE/api/v1/analytics/valuation/comps/$TICKER" -H "$AUTH_HEADER" | jq .

echo "--- LBO Model (60% debt) ---"
curl -s "$BASE/api/v1/analytics/valuation/lbo/$TICKER?debt=0.60&exit_year=5&exit_multiple=10" \
  -H "$AUTH_HEADER" | jq .

echo "--- Scenario Stress Test ---"
curl -s "$BASE/api/v1/analytics/scenario/$TICKER" -H "$AUTH_HEADER" | jq .

echo "--- Dividend Info ---"
curl -s "$BASE/api/v1/analytics/dividends/$TICKER" -H "$AUTH_HEADER" | jq .
