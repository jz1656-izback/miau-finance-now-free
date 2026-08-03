#!/usr/bin/env bash
# Miau Finance — Developer API examples
# Usage: ./sdk/curl/developer.sh
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

echo "=== Developer & API Keys ==="
echo ""

echo "--- Developer dashboard ---"
curl -s "$BASE/api/v1/developer/dashboard" -H "$AUTH_HEADER" | jq .

echo "--- List API keys ---"
curl -s "$BASE/api/v1/developer/api-keys" -H "$AUTH_HEADER" | jq .

echo "--- Create API key ---"
curl -s -X POST "$BASE/api/v1/developer/api-keys" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"name":"curl-example-key","scopes":["read"]}' | jq .

echo "--- List webhooks ---"
curl -s "$BASE/api/v1/developer/webhooks" -H "$AUTH_HEADER" | jq .

echo "--- Audit logs ---"
curl -s "$BASE/api/v1/audit/logs?limit=5" -H "$AUTH_HEADER" | jq .

echo "--- Audit export (CSV) ---"
curl -s -o /tmp/audit_export.csv "$BASE/api/v1/audit/export?format=csv" -H "$AUTH_HEADER"
echo "Exported to /tmp/audit_export.csv ($(wc -c < /tmp/audit_export.csv) bytes)"

echo "--- List registered brokers ---"
curl -s "$BASE/api/v1/brokers" -H "$AUTH_HEADER" | jq .
