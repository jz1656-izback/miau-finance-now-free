#!/usr/bin/env bash
# Social & Community API examples
# Usage: bash social.sh
set -euo pipefail
cd "$(dirname "$0")"
source ./setup.sh

echo "=== Social Feed ==="
curl -s "$BASE/api/v1/social/feed" -H "$AUTH_HEADER" | jq .

echo -e "\n=== My Activity ==="
curl -s "$BASE/api/v1/social/activity" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Followers ==="
curl -s "$BASE/api/v1/social/followers" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Following ==="
curl -s "$BASE/api/v1/social/following" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Shared Portfolios ==="
curl -s "$BASE/api/v1/portfolios/shared" -H "$AUTH_HEADER" | jq .

echo -e "\n=== Notifications ==="
curl -s "$BASE/api/v1/notifications/subscriptions" -H "$AUTH_HEADER" | jq .
