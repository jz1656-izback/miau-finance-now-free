# Miau Finance — Developer Portal

> Everything you need to build on Miau Finance.
> SDKs, plugins, API versioning, webhooks, rate limits, and best practices.

---

## Contents

1. [Getting Started](#getting-started)
2. [SDK Quick Links](#sdk-quick-links)
3. [API Versioning](#api-versioning)
4. [Rate Limits](#rate-limits)
5. [Webhooks](#webhooks)
6. [Error Handling](#error-handling)
7. [API Key Management](#api-key-management)
8. [Best Practices](#best-practices)

---

## Getting Started

1. **Get an API key**: `apikey create MyApp` in the terminal
2. **Install the SDK**: `pip install miau-finance` or `npm install miau-finance`
3. **Make your first call**: See [SDK Quickstart](../sdk/README.md)
4. **Check your rate limit**: `curl -H "Authorization: Bearer $KEY" /api/v1/developer/rate-limit`

```python
from miau import MiauClient
client = MiauClient(api_key="miau_your_key_here")
print(client.market.get_price("AAPL"))
```

## SDK Quick Links

| SDK | Language | Install | Status |
|-----|----------|---------|--------|
| [Python SDK](../sdk/README.md) | Python 3.10+ | `pip install miau-finance` | ✅ |
| [JavaScript SDK](../sdk/README.md) | Node 18+ / Browser | `npm install miau-finance` | ✅ |
| [curl examples](../sdk/curl/) | Shell | — | ✅ |
| [Plugin API](./PLUGIN_API.md) | Python | `plugin install <name>` | ✅ |

## API Versioning

### Current Version

The API currently operates at version **1** (`/api/v1/`).

### Versioning Strategy

- **Major version changes** (v1 → v2): Breaking changes. Deprecate v1, migrate to v2.
- **Minor changes**: New endpoints, new fields. No breaking changes.
- **Patch changes**: Bug fixes, performance improvements. No API changes.

### Accept-Version Header

You can specify the API version via the `Accept-Version` header:

```bash
curl -H "Accept-Version: 1" /api/v1/market/live?tickers=AAPL
```

If omitted, you get the current stable version.

### Deprecation Policy

- Major API versions are supported for 6 months after a new major version ships
- Deprecated endpoints return a `Warning: deprecation` header
- A changelog is provided for all breaking changes

```bash
# You'll see this header when an endpoint is deprecated:
# Warning: deprecation — "Use /api/v2/market/live instead"
```

## Rate Limits

### Per-Tier Limits

| Tier | Requests/Min | Requests/Hour | Burst |
|------|-------------|---------------|-------|
| Free | 20 | 500 | 5 |
| Pro | 100 | 5,000 | 20 |
| Enterprise | 10,000 | 100,000 | 500 |

### Rate Limit Headers

Every response includes your current rate limit status:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1623456789
```

### Checking Your Limits

```bash
curl -H "Authorization: Bearer $MIAU_API_KEY" \
  "http://localhost:8000/api/v1/developer/rate-limit"
```

Response:
```json
{
  "tier": "pro",
  "requests_per_minute": 100,
  "requests_per_hour": 5000,
  "remaining_minute": 87,
  "remaining_hour": 4230,
  "reset_minute": 1623456789,
  "reset_hour": 1623460000
}
```

### Handling 429 Responses

When you exceed your rate limit, the API returns HTTP 429 with a `Retry-After` header:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 45
```

Your SDK handles this automatically with exponential backoff:

```python
# SDK retries with: 1s, 2s, 4s, 8s backoff (configurable max retries)
order = client.trading.create_order("AAPL", "buy", 100, "market")
```

## Webhooks

Webhooks let you receive real-time events from Miau Finance.

### Creating a Webhook

```bash
curl -X POST -H "Authorization: Bearer $MIAU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://my.app/webhooks/miau","events":["trade.filled","alert.triggered"]}' \
  "http://localhost:8000/api/v1/webhooks"
```

### Supported Events

| Event | Triggered When |
|-------|----------------|
| `trade.filled` | An order is completely or partially filled |
| `trade.pending` | A new order is submitted |
| `trade.cancelled` | An order is cancelled |
| `alert.triggered` | A user's price alert condition is met |
| `portfolio.shared` | A portfolio share link is created |
| `ai.analysis.complete` | An AI analysis finishes |
| `subscription.changed` | User changes subscription tier |

### Webhook Payload

```json
{
  "event": "trade.filled",
  "timestamp": "2026-05-19T12:00:00Z",
  "data": {
    "order_id": "uuid",
    "ticker": "AAPL",
    "side": "BUY",
    "quantity": 100,
    "price": 186.90,
    "filled_at": "2026-05-19T12:00:00Z"
  }
}
```

### Webhook Signatures

Every webhook includes a signature header for verification:

```http
X-Miau-Signature: whsec_uuid_timestamp_sha256hex
X-Miau-Timestamp: 1712345678
```

Verify in your app:

```python
import hmac, hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"whsec_{expected}", signature)
```

### Testing Webhooks

Use the developer console to send a test webhook:

```bash
devconsole
# → Click "Test Webhook" → Select event → "Send"
```

Or via curl:

```bash
curl -X POST -H "Authorization: Bearer $MIAU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"webhook_id":"wh_uuid","event":"trade.filled"}' \
  "http://localhost:8000/api/v1/webhooks/test"
```

## Error Handling

### Error Response Format

All API errors return consistent JSON:

```json
{
  "detail": "Human-readable error message",
  "code": "ERROR_CODE",
  "params": {"field": "ticker", "value": "INVALID"},
  "docs": "https://miau.finance/docs/errors#INVALID_TICKER"
}
```

### Common Error Codes

| HTTP Status | Error Code | Meaning |
|-------------|-----------|---------|
| 400 | `INVALID_PARAMS` | Missing or invalid parameters |
| 401 | `NOT_AUTHENTICATED` | No or expired API key |
| 403 | `FORBIDDEN` | API key lacks required scope |
| 404 | `NOT_FOUND` | Resource doesn't exist |
| 422 | `VALIDATION_ERROR` | Request body validation failed |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Something went wrong on our end |
| 502 | `UPSTREAM_ERROR` | Upstream data source failed |

### SDK Error Handling

```python
from miau import MiauClient, AuthenticationError, RateLimitError

client = MiauClient(api_key="miau_key")

try:
    price = client.market.get_price("AAPL")
except AuthenticationError:
    print("🔑 Check your API key")
except RateLimitError:
    print("⏳ That's enough for now. Take a nap — like a cat.")
except Exception as e:
    print(f"❌ {e}")
```

## API Key Management

### Creating Keys

```bash
apikey create "My Trading Bot"
# → 🔑 Key: miau_a1b2c3d4e5f6...  (shown once)

# With specific permissions
apikey create "Analytics Only" --scopes "market:read,analytics:all"
```

### Key Scopes

| Scope | Access |
|-------|--------|
| `market:read` | Read market data (prices, history, crypto, forex) |
| `market:write` | Place orders |
| `portfolio:read` | Read portfolio data |
| `portfolio:write` | Create/modify portfolios |
| `analytics:all` | Full analytics access |
| `social:read` | Read social feed |
| `social:write` | Create posts, follow users |
| `billing:read` | Read subscription info |
| `admin:all` | Full admin access (requires admin role) |

### Key Rotation

```bash
# Revoke old key
apikey revoke miau_a1b2c3d4

# Create new key
apikey create "My Trading Bot v2"

# Update your application with the new key
```

## Best Practices

### 1. Use API Keys with Minimum Required Scopes

```python
# Too broad:
# SCOPES: admin:all

# Better:
SCOPES: market:read, portfolio:read
```

### 2. Implement Exponential Backoff

```python
import time
import random

def call_with_retry(client, method, *args, max_retries=3):
    for attempt in range(max_retries):
        try:
            return method(*args)
        except RateLimitError:
            wait = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait)
    raise Exception("Max retries exceeded")
```

### 3. Cache Market Data

```python
# Market data changes every ~15 seconds
# Cache it for 30 seconds to stay within rate limits
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def get_cached_price(ticker: str):
    return client.market.get_price(ticker)
```

### 4. Use Webhooks Instead of Polling

Instead of polling `/api/v1/orders` every 5 seconds:
```python
# Bad — expensive polling
while True:
    orders = client.trading.list_orders()
    time.sleep(5)
```

Register a webhook for `trade.filled` events:
```python
# Good — event-driven
# POST /api/v1/webhooks → event: trade.filled
# Your endpoint receives the event when it happens
```

### 5. Handle Idempotency for Order Creation

```python
from uuid import uuid4

def create_order_safe(client, ticker, side, qty, idempotency_key=None):
    headers = {}
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    return client.trading.create_order(ticker, side, qty, "market", headers=headers)

# Call with same idempotency_key → guaranteed at-most-once
order = create_order_safe(client, "AAPL", "buy", 100, str(uuid4()))
```

---

*Built with 🐱 for developers who prefer keyboards to KPI meetings.*
*Rate limits exist to protect your cat from too much screen time.*
