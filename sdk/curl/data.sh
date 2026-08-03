#!/usr/bin/env bash
# Currencies, Instruments & Watchlist API examples
# Usage: bash data.sh
set -euo pipefail
cd "$(dirname "$0")"
source auth.sh

echo "=== List Currencies ==="
miau_curl GET "/currencies"

echo -e "\n=== Currency Detail ==="
miau_curl GET "/currencies/USD"

echo -e "\n=== Convert Currency ==="
miau_curl GET "/currencies/convert?from=USD&to=EUR&amount=1000"

echo -e "\n=== List Instruments ==="
miau_curl GET "/instruments"

echo -e "\n=== Instrument Detail ==="
miau_curl GET "/instruments/{id}" 2>/dev/null || echo "Replace {id} with instrument UUID"

echo -e "\n=== Instrument Market Data ==="
miau_curl GET "/instruments/{id}/market-data" 2>/dev/null || echo "Replace {id}"

echo -e "\n=== Sectors ==="
miau_curl GET "/instruments/sectors/list"

echo -e "\n=== Instrument Types ==="
miau_curl GET "/instruments/types/list"

echo -e "\n=== Search ==="
miau_curl GET "/search?q=AAPL"

echo -e "\n=== Watchlist ==="
miau_curl GET "/watchlist/items"

echo -e "\n=== Add to Watchlist ==="
miau_curl POST "/watchlist/items" -d '{"ticker": "AAPL"}'

echo -e "\n=== Delete from Watchlist ==="
miau_curl DELETE "/watchlist/items?ticker=AAPL"

echo -e "\n=== Alerts ==="
miau_curl GET "/alerts"

echo -e "\n=== Create Alert ==="
miau_curl POST "/alerts" -d '{"name": "AAPL target", "ticker": "AAPL", "condition": "price > 250", "severity": "high"}'

echo -e "\n=== Fundamentals ==="
miau_curl GET "/fundamentals/AAPL"

echo -e "\n=== Economics (FRED) ==="
miau_curl GET "/economics/fred?series_ids=GDP,CPIAUCSL&limit=100"
