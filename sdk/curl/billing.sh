#!/usr/bin/env bash
# Billing & API Keys API examples
# Usage: bash billing.sh
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

echo "=== Get Subscription ==="
curl -s "$BASE/api/v1/billing/subscription" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Billing History ==="
curl -s "$BASE/api/v1/billing/history" -H "$AUTH_HEADER" | jq .

echo -e "\n=== List API Keys ==="
curl -s "$BASE/api/v1/api-keys" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Create API Key ==="
curl -s -X POST "$BASE/api/v1/api-keys" \
  -H "Content-Type: application/json" -H "$AUTH_HEADER" \
  -d '{"name": "My App Key", "scopes": ["market:read", "orders:create"], "expires_in_days": 365}' | jq .

echo -e "\n=== Webhook Endpoints ==="
curl -s "$BASE/api/v1/webhooks" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Create Webhook ==="
curl -s -X POST "$BASE/api/v1/webhooks" \
  -H "Content-Type: application/json" -H "$AUTH_HEADER" \
  -d '{"url": "https://myapp.com/webhook", "events": ["order.filled", "price.alert"]}' | jq .

echo -e "\n=== Developer Dashboard ==="
curl -s "$BASE/api/v1/developer/dashboard" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Audit Logs ==="
curl -s "$BASE/api/v1/audit/logs?limit=5" -H "$AUTH_HEADER" | jq .
