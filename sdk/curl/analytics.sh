#!/usr/bin/env bash
# Miau Finance — Analytics API examples
# Usage: ./sdk/curl/analytics.sh [ticker]
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

TICKER="${1:-AAPL}"

echo "=== Analytics ==="
echo ""

echo "--- Portfolio analytics ---"
curl -s "$BASE/api/v1/analytics/summary" -H "$AUTH_HEADER" | jq .

echo "--- Risk: Value at Risk (95%) ---"
curl -s "$BASE/api/v1/risk/var?ticker=$TICKER&confidence=0.95" -H "$AUTH_HEADER" | jq .

echo "--- Risk: Beta vs SPY ---"
curl -s "$BASE/api/v1/risk/beta?ticker=$TICKER&benchmark=SPY" -H "$AUTH_HEADER" | jq .

echo "--- Risk: Stress test ---"
curl -s "$BASE/api/v1/risk/stress-test?ticker=$TICKER" -H "$AUTH_HEADER" | jq .

echo "--- Risk: Greeks (ATM call) ---"
curl -s "$BASE/api/v1/risk/greeks?spot=100&strike=100&days_to_expiry=30&volatility=0.25" \
  -H "$AUTH_HEADER" | jq .

echo "--- Risk: Comprehensive ---"
curl -s "$BASE/api/v1/risk/comprehensive?ticker=$TICKER" -H "$AUTH_HEADER" | jq .

echo "--- Risk: Rolling metrics ---"
curl -s "$BASE/api/v1/risk/rolling?ticker=$TICKER&window=12mo&period=3y" -H "$AUTH_HEADER" | jq .

echo "--- Factor analysis ---"
curl -s "$BASE/api/v1/analytics/factors/$TICKER?model=3factor&period=2y" -H "$AUTH_HEADER" | jq .

echo "--- Monte Carlo simulation ---"
curl -s "$BASE/api/v1/analytics/monte-carlo?ticker=$TICKER&num_simulations=500&days=252" \
  -H "$AUTH_HEADER" | jq .

echo "--- Sentiment analysis ---"
curl -s "$BASE/api/v1/analytics/sentiment?ticker=$TICKER&days=7" -H "$AUTH_HEADER" | jq .

echo "--- Options chain ---"
curl -s "$BASE/api/v1/options/$TICKER" -H "$AUTH_HEADER" | jq .
