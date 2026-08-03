#!/usr/bin/env bash
# AI & Advanced Analytics API examples
# Usage: bash ai.sh
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

echo "=== AI Advisor — Portfolio Analysis ==="
curl -s -X POST "$BASE/api/v1/ai/advisor/portfolio" \
  -H "Content-Type: application/json" -H "$AUTH_HEADER" \
  -d '{"holdings": [{"ticker": "AAPL", "value": 50000}, {"ticker": "MSFT", "value": 30000}]}' | jq .

echo -e "\n=== AI Market Analysis ==="
curl -s -X POST "$BASE/api/v1/ai/advisor/market" \
  -H "Content-Type: application/json" -H "$AUTH_HEADER" \
  -d '{"query": "What sectors are outperforming this quarter?"}' | jq .

echo -e "\n=== AI Risk Assessment ==="
curl -s -X POST "$BASE/api/v1/ai/advisor/risk" \
  -H "Content-Type: application/json" -H "$AUTH_HEADER" \
  -d '{"tickers": ["AAPL", "MSFT", "SPY"]}' | jq .

echo -e "\n=== AI Query ==="
curl -s -X POST "$BASE/api/v1/ai/query" \
  -H "Content-Type: application/json" -H "$AUTH_HEADER" \
  -d '{"query": "What is my portfolio risk?"}' | jq .

echo -e "\n=== Sentiment Analysis ==="
curl -s "$BASE/api/v1/analytics/sentiment?ticker=AAPL&days=7" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Monte Carlo Simulation ==="
curl -s "$BASE/api/v1/analytics/monte-carlo?ticker=AAPL&num_simulations=1000&days=252" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Options Chain ==="
curl -s "$BASE/api/v1/options/AAPL" -H "$AUTH_HEADER" | jq .
