# Miau Finance SDK

> Python + JavaScript + curl SDK for the Miau Finance API.
> Install in seconds. Build in minutes. Trade like a cat.

---

## Quick Install

### Python
```bash
pip install miau-finance
```

### JavaScript / TypeScript
```bash
npm install miau-finance
```

### curl
```bash
# Copy your API key from the dev console, then:
export MIAU_API_KEY="miau_your_key_here"
```

---

## Python SDK

### Quick Start

```python
from miau import MiauClient

client = MiauClient(api_key="miau_your_key_here")

# Market data
price = client.market.get_price("AAPL")
print(f"AAPL: ${price['price']}")

# Portfolio
portfolios = client.portfolio.list()
portfolio = client.portfolio.get(portfolios[0]["id"])

# Trading
order = client.trading.create_order("AAPL", "buy", 100, "market")

# AI Advisor
advice = client.ai.portfolio_analysis(portfolio["id"])

# Social
feed = client.social.get_feed()
leaderboard = client.social.get_leaderboard()

# Currencies
currencies = client.currencies.list()
converted = client.currencies.convert(100, "USD", "EUR")
```

### Async Support

```python
import asyncio
from miau import AsyncMiauClient

async def main():
    client = AsyncMiauClient(api_key="miau_your_key_here")
    price = await client.market.get_price("AAPL")
    print(price)

asyncio.run(main())
```

### Available Modules

| Module | Methods | Description |
|--------|---------|-------------|
| `client.market` | `get_price`, `get_history`, `get_crypto`, `get_forex` | Market data |
| `client.portfolio` | `list`, `get`, `create`, `update`, `delete` | Portfolio management |
| `client.trading` | `create_order`, `list_orders`, `cancel_order`, `paper_trade`, `list_strategies`, `run_backtest` | Trading & backtesting |
| `client.ai` | `portfolio_analysis`, `market_overview`, `risk_assessment`, `ask_query` | AI advisor |
| `client.social` | `share_portfolio`, `get_leaderboard`, `get_feed`, `follow`, `get_profile`, `get_reputation` | Social features |
| `client.currencies` | `list`, `convert`, `get_rates` | Multi-currency |
| `client.analytics` | `risk`, `attribution`, `dcf`, `lbo`, `comps`, `wacc`, `scenario` | Advanced analytics |
| `client.billing` | `get_subscription`, `create_checkout` | Subscriptions |

---

## JavaScript SDK

### Quick Start

```javascript
import { MiauClient } from 'miau-finance'

const client = new MiauClient({ apiKey: 'miau_your_key_here' })

// Market data
const price = await client.market.getPrice('AAPL')
console.log(`AAPL: $${price.price}`)

// Portfolio
const portfolios = await client.portfolio.list()
const portfolio = await client.portfolio.get(portfolios[0].id)

// Trading
const order = await client.trading.createOrder('AAPL', 'buy', 100, 'market')

// AI
const advice = await client.ai.portfolioAnalysis(portfolio.id)

// Currencies
const currencies = await client.currencies.list()
const converted = await client.currencies.convert(100, 'USD', 'EUR')
```

---

## curl Examples

```bash
# Set your key
export MIAU_API_KEY="miau_your_key_here"

# Market data
curl -H "Authorization: Bearer $MIAU_API_KEY" \
  "http://localhost:8000/api/v1/market/live?tickers=AAPL,MSFT"

# Portfolio
curl -H "Authorization: Bearer $MIAU_API_KEY" \
  "http://localhost:8000/api/v1/portfolios"

# Trading
curl -X POST -H "Authorization: Bearer $MIAU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"AAPL","side":"BUY","quantity":10,"order_type":"market"}' \
  "http://localhost:8000/api/v1/orders"

# Currencies
curl -H "Authorization: Bearer $MIAU_API_KEY" \
  "http://localhost:8000/api/v1/currencies/rates"

# AI
curl -X POST -H "Authorization: Bearer $MIAU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  "http://localhost:8000/api/v1/ai/advisor/market"
```

See the [`sdk/curl/`](./curl/) directory for 14+ shell scripts covering all major endpoints.

---

## Rate Limits

| Tier | Requests/Min | Requests/Hour |
|------|-------------|---------------|
| Free | 20 | 500 |
| Pro | 100 | 5,000 |
| Enterprise | 10,000 | 100,000 |

Check your rate limit status:
```bash
curl -H "Authorization: Bearer $MIAU_API_KEY" \
  "http://localhost:8000/api/v1/developer/rate-limit"
```

---

## Error Handling

All SDK methods throw typed errors:

| Error | HTTP Status | Meaning |
|-------|-------------|---------|
| `AuthenticationError` | 401 | Invalid or missing API key |
| `RateLimitError` | 429 | Too many requests |
| `ValidationError` | 422 | Invalid parameters |
| `NotFoundError` | 404 | Resource not found |
| `ApiError` | 5xx | Server error |

---

## SDK Versioning

SDK versions follow [semver](https://semver.org/):

- **Major**: Breaking API changes
- **Minor**: New features, backwards compatible
- **Patch**: Bug fixes

See [`CHANGELOG.md`](./CHANGELOG.md) for version history.

---

## Need Help?

- [API Reference](../docs/API.md) — Complete endpoint documentation
- [Plugin Guide](../docs/PLUGIN_API.md) — Build plugins for Miau Finance
- [Developer Portal](../docs/DEVELOPER_PORTAL.md) — Rate limits, webhooks, versioning
- [GitHub Issues](https://github.com/LuZziD/cat-finance-analytics-shell-miau/issues) — Report bugs, request features

---

*Built with 🐱 by traders who prefer purrs to CNBC*
