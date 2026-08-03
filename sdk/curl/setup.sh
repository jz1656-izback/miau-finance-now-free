#!/usr/bin/env bash
# Miau Finance — curl examples setup
# Source this file to set up auth variables:
#   source sdk/curl/setup.sh
# Then run any example: ./sdk/curl/market.sh

export BASE="${BASE:-http://localhost:8000}"

# Get an API key from your dev console or use JWT auth
# Option 1: API key (recommended for scripts)
export API_KEY="${API_KEY:-miau_your_api_key_here}"

# Option 2: JWT token (from login)
# export JWT_TOKEN=$(curl -s -X POST "$BASE/api/v1/auth/token" \
#   -H "Content-Type: application/json" \
#   -d '{"username":"dev_user","password":"dev_pass"}' | jq -r '.access_token')

if [ "$API_KEY" != "miau_your_api_key_here" ]; then
    export AUTH_HEADER="Authorization: Bearer $API_KEY"
else
    export AUTH_HEADER="${AUTH_HEADER:-}"
fi

echo "Miau Finance API: $BASE"
echo "Auth: ${AUTH_HEADER:+set (${API_KEY:0:12}...)}${AUTH_HEADER:-NOT SET — export API_KEY or JWT_TOKEN}"
echo ""
