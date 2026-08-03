# 🐱 Miau Finance Developer Guide

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "The inner workings. For cats who build."
```

This guide covers the internal architecture, conventions, and patterns for contributing code to Miau Finance. If you're setting up for the first time, see [TUTORIAL.md](./TUTORIAL.md). If you want to contribute, see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 🏗️ Project Structure

```
miau-finance/
├── frontend/                    # React 18 + Vite + TypeScript
│   ├── src/
│   │   ├── components/          # UI components
│   │   │   ├── Terminal.tsx     # Main terminal shell (107 KB)
│   │   │   ├── WorldMap.tsx     # 3D globe + flat map (27 KB)
│   │   │   ├── Heatmap.tsx      # Sector/correlation heatmap
│   │   │   ├── SplitTerminal.tsx # Tmux-style split panes
│   │   │   ├── Transitions.tsx  # Loading animations
│   │   │   └── layout/          # Layout components
│   │   ├── lib/
│   │   │   ├── commands.ts      # All terminal commands (43 KB)
│   │   │   ├── api.ts           # API client
│   │   │   └── catSounds.ts     # Cat sound effects
│   │   ├── design/
│   │   │   └── tokens.ts        # Design system tokens
│   │   ├── types/               # TypeScript type definitions
│   │   ├── index.css            # Global styles + CRT effects
│   │   └── App.tsx              # Root component
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── backend/                     # FastAPI + Python 3.11+
│   ├── app/
│   │   ├── main.py              # App factory, middleware, route mounting
│   │   ├── config.py            # Settings (env vars, secrets)
│   │   ├── metrics.py           # Prometheus metrics
│   │   ├── cache.py             # Redis caching layer
│   │   ├── seed.py              # Database seeder
│   │   ├── api/                 # Route handlers (endpoints)
│   │   │   ├── analytics/       # Analytics endpoints (12 modules)
│   │   │   │   ├── market.py, optimizer.py, risk.py
│   │   │   │   ├── signals.py, reports.py, combined.py
│   │   │   │   ├── news.py, sentiment.py, fundamentals.py
│   │   │   │   ├── economics.py, fred.py, options.py, monte_carlo.py
│   │   │   ├── instruments.py   # Financial instruments CRUD
│   │   │   ├── ontology.py      # Dynamic type system
│   │   │   ├── portfolios.py    # Portfolio management
│   │   │   ├── trades.py        # Trade execution
│   │   │   ├── search.py        # Search endpoint
│   │   │   ├── pipelines.py     # ETL/transform pipeline status
│   │   │   └── ws.py            # WebSocket price streaming
│   │   ├── services/            # Business logic layer
│   │   │   ├── analytics/       # Analytics engines
│   │   │   │   ├── monte_carlo.py, black_litterman.py
│   │   │   │   └── sentiment.py
│   │   │   └── data_sources/    # External data integrations
│   │   │       ├── sec_edgar.py, fred.py
│   │   │       ├── options.py, insider.py
│   │   │       └── technical.py, fundamental.py, economic.py
│   │   ├── middleware/          # Security middleware
│   │   │   ├── auth.py, rate_limit.py
│   │   │   ├── security_headers.py, sanitize.py
│   │   │   └── __init__.py
│   │   ├── schemas/             # Pydantic request/response models
│   │   └── models/              # SQLAlchemy DB models
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Backend container
│   └── tests/                   # pytest test suite
│
├── docker-compose.yml           # Full stack orchestration
├── Makefile                     # Common dev commands
├── .env / .env.example          # Environment config
│
├── k8s/                         # Kubernetes manifests
│   ├── deployment.yaml, service.yaml, ingress.yaml
│   ├── frontend.yaml, redis.yaml, postgres.yaml
│   ├── namespace.yaml, configmap.yaml, secret.yaml
│
├── grafana/                     # Grafana config
│   ├── dashboards/miau.json     # Pre-built dashboard
│   └── datasources/prometheus.yaml
│
├── prometheus/
│   └── prometheus.yml           # Scrape config
│
├── airflow/, cube/, dbt/        # ETL & BI
├── minio/, postgres/, superset/  # Infrastructure
│
└── docs/                        # Documentation
    ├── API.md, COMMANDS.md, ARCHITECTURE.md
    ├── CONTRIBUTING.md, TUTORIAL.md, DEVELOPER.md
    ├── SECURITY.md, GLOSSARY.md
```

---

## 🔄 Data Flows

### Market Data Flow

```
External APIs (Yahoo Finance, CoinGecko, FRED, SEC)
    │
    ▼
backend/app/services/data_sources/ (httpx async, retry, cache)
    │
    ▼
backend/app/services/analytics/ (compute signals, risk, sentiment)
    │
    ▼
backend/app/api/ (FastAPI endpoints /api/v1/market/*)
    │
    ├──▶ HTTP ──▶ frontend/src/lib/api.ts ──▶ Terminal output
    │
    └──▶ WebSocket (ws://localhost:8000/api/v1/ws/prices)
            ──▶ Real-time price updates in terminal
```

### Command Execution Flow

```
User types: "price AAPL"
    │
    ▼
Terminal.tsx: handleInput("price AAPL")
    │
    ▼
commands.ts: processCommand("price", ["AAPL"])
    │
    ▼
api.ts: GET /api/v1/market/price/AAPL
    │
    ▼
main.py: router → instruments.py: get_price("AAPL")
    │
    ▼
data_sources/market_service.py: fetch AAPL (cache → API)
    │
    ▼
Return PriceResponse → Format output → Render in terminal
```

---

## 🧩 How to Add a Backend Endpoint

### 1. Create the data source service

```python
# backend/app/services/data_sources/my_source.py
import httpx
from app.cache import cache

async def fetch_my_data(symbol: str) -> dict:
    """Fetch data from external API with retry and cache."""
    cache_key = f"my_source:{symbol}"
    cached = await cache.get(cache_key)
    if cached:
        return cached

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://api.example.com/{symbol}")
        data = resp.json()

    await cache.set(cache_key, data, ttl=300)  # 5 min TTL
    return data
```

### 2. Create the API endpoint

```python
# backend/app/api/my_source.py
from fastapi import APIRouter, HTTPException, Query
from app.services.data_sources.my_source import fetch_my_data

router = APIRouter()

@router.get("/{symbol}")
async def get_my_data(
    symbol: str,
    period: str = Query("3mo", regex="^(1mo|3mo|6mo|1y)$")
):
    try:
        data = await fetch_my_data(symbol)
        return {"symbol": symbol, "data": data}
    except Exception as e:
        raise HTTPException(500, detail=str(e))
```

### 3. Mount the router in main.py

```python
# backend/app/main.py
from app.api import my_source

app.include_router(
    my_source.router,
    prefix="/api/v1/my-source",
    tags=["My Source"],
    dependencies=auth_deps
)
```

### 4. Add to tests

```python
# backend/tests/test_api/test_my_source.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_my_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get(
            "/api/v1/my-source/AAPL",
            headers={"Authorization": "Bearer test_token"}
        )
    assert resp.status_code == 200
    assert "symbol" in resp.json()
```

### 5. Document it

Add to `docs/API.md`:

```markdown
### `GET /api/v1/my-source/{symbol}`

Returns my custom data for the given symbol.

**Parameters:**
- `symbol` (path, required) — Stock ticker
- `period` (query, optional) — Time period. Default: `3mo`

**Response:**
\`\`\`json
{
  "symbol": "AAPL",
  "data": { ... }
}
\`\`\`
```

---

## 🧩 How to Add a Terminal Command

### 1. Add the command handler in commands.ts

```typescript
// frontend/src/lib/commands.ts

// In the processCommand function add:
case 'mycommand': {
  const symbol = args[0] || 'AAPL'
  if (!symbol || symbol.match(/[^A-Z]/)) {
    addLines([{ text: '😿 Invalid symbol. Usage: mycommand <TICKER>', className: 'text-red' }])
    break
  }
  addLines([{ text: `🐱 Loading data for ${symbol}...`, className: 'text-dim italic' }])
  try {
    const res = await api.get(`/my-source/${symbol}`)
    const data = res.data
    addLines([
      { text: `😸 ${data.symbol} — Custom Data`, className: 'text-green font-bold' },
      { text: JSON.stringify(data.data, null, 2), className: 'text-cyan' }
    ])
  } catch (e) {
    addLines([{ text: `😿 Failed to fetch data: ${e}`, className: 'text-red' }])
  }
  break
}
```

### 2. Add to autocomplete

```typescript
// In getAutocompleteOptions() add:
options.push(
  { label: 'mycommand', description: 'My custom command' }
)
```

### 3. Add to help text

```typescript
// In the 'help' case add:
{ text: '  mycommand <ticker>  — My custom command', className: 'text-green' },
```

### 4. Update docs/COMMANDS.md

```markdown
#### `mycommand <ticker>`

Performs my custom operation on the given ticker.

**Example:**
`mycommand AAPL`
```

---

## 🧩 How to Add a Frontend Component

### 1. Create the component

```tsx
// frontend/src/components/MyComponent.tsx
import React, { useRef, useEffect } from 'react'

interface MyComponentProps {
  data: MyData[]
  onClose?: () => void
}

const MyComponent: React.FC<MyComponentProps> = ({ data, onClose }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const ctx = canvasRef.current?.getContext('2d')
    if (!ctx) return
    // Canvas rendering...
  }, [data])

  return (
    <div className="absolute inset-0 z-50">
      <canvas ref={canvasRef} width={window.innerWidth} height={window.innerHeight} />
      {onClose && (
        <button onClick={onClose} className="absolute top-2 right-2 text-green hover:text-cyan">
          ✕
        </button>
      )}
    </div>
  )
}

export default MyComponent
```

### 2. Wire into Terminal.tsx

```tsx
// In Terminal.tsx
import MyComponent from './MyComponent'

// In render:
{showMyComponent && <MyComponent data={myData} onClose={() => setShowMyComponent(false)} />}
```

### 3. Trigger with a command

```typescript
// In commands.ts
case 'mycomponent':
  terminalRef.showMyComponent = true
  addLines([{ text: 'Component activated!', className: 'text-cyan' }])
  break
```

---

## 🗄️ Database Schema

### Core Tables

| Table | Purpose | Key Columns |
|-------|---------|------------|
| `objects` | Ontology — universal entity store | `id, external_id, type_id, data(jsonb)` |
| `object_types` | Type definitions | `id, name, schema(jsonb)` |
| `portfolios` | Portfolio metadata | `id, name, created_at` |
| `portfolio_positions` | Portfolio holdings | `portfolio_id, ticker, shares, avg_price` |
| `trades` | Trade history | `id, portfolio_id, ticker, side, quantity, price, timestamp` |
| `market_data` | Historical prices | `ticker, date, open, high, low, close, volume` |
| `watchlists` | (planned) | `user_id, name` |

---

## 🔐 Security Architecture

```
Request
    │
    ▼
┌──────────────┐
│ CORS         │ → Restrict origins
└──────────────┘
    │
    ▼
┌──────────────┐
│ Security     │ → CSP, X-Frame-Options, HSTS headers
│ Headers      │
└──────────────┘
    │
    ▼
┌──────────────┐
│ Rate Limit   │ → 100 req/min/IP, 1000 req/hr/user
└──────────────┘
    │
    ▼
┌──────────────┐
│ JWT Auth     │ → Bearer token validation
└──────────────┘
    │
    ▼
┌──────────────┐
│ Input        │ → Pydantic validation + HTML sanitize
│ Validation   │
└──────────────┘
    │
    ▼
  Handler
```

See [SECURITY.md](./SECURITY.md) for full security documentation.

---

## 📊 Monitoring Stack

| Component | Endpoint | Purpose |
|-----------|----------|---------|
| **Health** | `GET /api/v1/health` | Service alive check |
| **Metrics** | `GET /metrics` | Prometheus scrape endpoint |
| **Grafana** | `http://localhost:3000` | Pre-built Miau dashboard |
| **Redis** | Internal | `redis_hits_total`, `redis_misses_total` |
| **HTTP Metrics** | Middleware | `http_requests_total`, `http_request_duration_seconds` |

---

## 🧪 Testing Strategy

```
backend/tests/
├── conftest.py          # Fixtures: test DB, auth token, seed data
├── test_api/            # API endpoint tests (one per module)
│   ├── test_instruments.py
│   ├── test_portfolios.py
│   ├── test_market.py
│   └── ...
└── test_services/       # Service layer tests
```

```bash
# Run all tests
make test-backend

# Run specific test file
docker compose exec backend python -m pytest tests/test_api/test_market.py -v

# Run with coverage
docker compose exec backend python -m pytest tests/ --cov=app --cov-report=term-missing
```

---

## 🐛 Debugging

### Backend logs

```bash
docker compose logs backend -f
```

### Database access

```bash
make psql
# or
docker compose exec postgres psql -U miau miau
```

### Redis inspection

```bash
docker compose exec redis redis-cli
> KEYS *
> GET cache:price:AAPL
```

### Frontend debugging

Open the browser console. All API calls and command executions are logged.

---

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "The code is the cat tree.
               Climb it. Explore it.
               But don't knock anything over."
```

---
_[Back to README](../README.md) | [Contributing](./CONTRIBUTING.md) | [Tutorial](./TUTORIAL.md)_
# 🐱 MIAU FINANCE — Developer Guide

## Quick Start for Developers
```bash
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd miau-finance
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

## Adding a Command
1. Add route in `backend/app/api/`
2. Register in `backend/app/main.py`
3. Add case in `frontend/src/lib/commands.ts`
4. Add help text
5. Write test in `frontend/tests/`

## Adding a Data Provider
1. Create `backend/app/services/data/providers/{name}.py`
2. Register in `backend/app/services/data/__init__.py`

## Standards
- **Python**: PEP 8, async-first, type hints
- **TypeScript**: strict mode, no `any`
- **Commits**: `[area] description`
- **Tests**: Write first, code second

## Structure
```
miau-finance/
├── backend/         # Python FastAPI
├── frontend/        # React/TypeScript
├── docs/            # 30+ doc files
├── k8s/             # Kubernetes
└── scripts/         # Go-live utilities
```

---
*Merged from DEVELOPER_GUIDE.md (V69)*

# 🐱 Miau Finance SDK & API Quickstart

```
  ╱|、
 (˚ˎ 。7
  |、˜〵
  じしˍ,)ノ    "The cat provides APIs.
               The cat provides SDKs.
               The cat provides no warranty."
```

Get started with the Miau Finance API in Python, JavaScript, or curl. For the full endpoint reference (150+ endpoints), see [API.md](./API.md).

---

## 🔐 Authentication

### Get a Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
   -d "username=your_username&password=your_password"
# → { "access_token": "eyJ...", "token_type": "bearer" }
```

### API Key (Recommended for Scripts)

Generate a key from the terminal: `apikey create "my-app"`
Then use it in headers:

```bash
curl http://localhost:8000/api/v1/market/live?tickers=AAPL \
  -H "Authorization: Bearer miau_abc123..."
```

---

## 🐍 Python SDK

### Install

```bash
pip install -e sdk/python
```

### Usage

```python
from miau import MiauClient

# Connect with API key or JWT token
api = MiauClient(api_key="miau_abc...")
# or: api = MiauClient(token="eyJ...")

# ── Market Data ──
price = api.get("/api/v1/market/live", params={"tickers": "AAPL,MSFT"})
history = api.get("/api/v1/market/historical/AAPL", params={"period": "6mo"})
sectors = api.get("/api/v1/market/sectors")
global_markets = api.get("/api/v1/markets/global")

# ── Portfolio ──
portfolios = api.get("/api/v1/portfolios")
positions = api.get("/api/v1/portfolios/{id}/positions")

# ── AI Advisor ──
advice = api.post("/api/v1/ai/query", body={"query": "Is AAPL a buy?"})

# ── Valuation (Investment Banking) ──
dcf = api.get("/api/v1/analytics/valuation/dcf/AAPL")
wacc = api.get("/api/v1/analytics/valuation/wacc/AAPL")
comps = api.get("/api/v1/analytics/valuation/comps/AAPL")
lbo = api.get("/api/v1/analytics/valuation/lbo/AAPL")
football = api.get("/api/v1/analytics/valuation/football/AAPL")
sensitivity = api.get("/api/v1/analytics/valuation/sensitivity/AAPL")

# ── ESG ──
esg = api.get("/api/v1/esg/AAPL")
carbon = api.get("/api/v1/carbon/AAPL")

# ── DeFi ──
protocols = api.get("/api/v1/defi/protocols")
wallet = api.get("/api/v1/defi/wallet")

# ── Quantum (v1.9.0+) ──
qubo = api.get("/api/v1/quantum/formulate")
anneal = api.get("/api/v1/quantum/anneal", params={"budget": 5})

# ── AGI (v2.0.0+) ──
hypotheses = api.get("/api/v1/agi/hypotheses", params={"ticker": "AAPL"})
```

### Sync client

```python
from miau import MiauSyncClient
api = MiauSyncClient(api_key="miau_abc...")
price = api.get("/api/v1/market/live", params={"tickers": "AAPL"})
```

---

## 📜 JavaScript/TypeScript SDK

```js
import { MiauClient } from './sdk/javascript/miau.js'

const api = new MiauClient({ apiKey: 'miau_abc...' })

// Promise-based
const price = await api.get('/api/v1/market/live', { tickers: 'AAPL' })
const dcf = await api.get('/api/v1/analytics/valuation/dcf/AAPL')
const esg = await api.get('/api/v1/esg/AAPL')

// Convenience methods
const portfolio = await api.portfolio.get('id-here')
const market = await api.market.live(['AAPL', 'MSFT'])
const ai = await api.ai.query('What should I buy?')
```

---

## 🖥️ curl SDK

Pre-built shell scripts in `sdk/curl/` for every endpoint category:

```bash
cd sdk/curl
source setup.sh                # Configure your API key

bash market.sh                 # Live prices, crypto, forex, sectors
bash portfolio.sh              # Portfolios, positions, analytics
bash trading.sh                # Orders, strategies, signals
bash ai.sh                     # AI advisor, sentiment, options
bash social.sh                 # Feed, follows, shares
bash billing.sh                # Subscriptions, API keys, webhooks
bash data.sh                   # Currencies, instruments, watchlist
```

Or run individual calls:

```bash
# List all currencies
curl http://localhost:8000/api/v1/currencies -H "Authorization: Bearer $TOKEN"

# Convert 100 USD to EUR
curl "http://localhost:8000/api/v1/currencies/convert?from=USD&to=EUR&amount=100" \
  -H "Authorization: Bearer $TOKEN"

# DCF valuation with custom parameters
curl "http://localhost:8000/api/v1/analytics/valuation/dcf/AAPL?growth=0.08&years=7" \
  -H "Authorization: Bearer $TOKEN"
```

---

## ⏱️ Rate Limits

| Tier | Requests/min | Requests/hour |
|------|-------------|---------------|
| **Free** | 60 | 1,000 |
| **Pro** | 100 | 5,000 |
| **Enterprise** | 10,000 | 100,000 |

Rate limit info is returned in response headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1716959770
```

Exceeding the limit returns **HTTP 429**:
```json
{"detail": "Tier rate limit exceeded (free: 60/min). Upgrade for more."}
```

---

## 🔔 Webhooks

Webhooks fire on events (order fills, price alerts, portfolio changes) with **HMAC-SHA256 signing**.

### Create a Webhook

```bash
curl -X POST http://localhost:8000/api/v1/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://myapp.com/hooks", "events": ["order.filled", "price.alert"]}'
# → { "id": "...", "signing_secret": "abc123...", ... }
```

### Verify Signatures

Every webhook delivery includes `X-Miau-Signature` header:
```python
import hmac, hashlib

def verify(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### Test a Webhook

```bash
curl -X POST http://localhost:8000/api/v1/webhooks/{id}/ping \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧩 Plugin Development

Build extensions that hook into the Miau Finance lifecycle. See [PLUGIN_API.md](./PLUGIN_API.md).

```python
from app.services.plugin.spec import PluginBase, PluginMeta, HookPoint

class MyPlugin(PluginBase):
    meta = PluginMeta(
        name="my-plugin",
        version="1.0.0",
        hooks=[HookPoint.AFTER_MARKET_DATA],
    )

    async def initialize(self): pass
    async def shutdown(self): pass

    async def after_market_data(self, data: dict, **kw) -> dict:
        data["enriched_by"] = "my-plugin"
        return data
```

---

## 📚 Reference

| Doc | What |
|-----|------|
| [API.md](./API.md) | Full endpoint reference (3,820 lines, 150+ endpoints) |
| [DEVELOPER.md](./DEVELOPER.md) | Internal architecture & conventions |
| [DEVELOPER_PORTAL.md](./DEVELOPER_PORTAL.md) | Developer onboarding & best practices |
| [PLUGIN_API.md](./PLUGIN_API.md) | Plugin development guide |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | How to contribute |
| [SECURITY.md](./SECURITY.md) | Security architecture |
| [SECURITY_AUDIT.md](./SECURITY_AUDIT.md) | Latest security audit (May 2026) |
| [TUTORIAL.md](./TUTORIAL.md) | Step-by-step tutorial |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System architecture diagram |
| [sdk/python/](../sdk/python/) | Python SDK source |
| [sdk/curl/](../sdk/curl/) | curl examples |

---
*Merged from DEVELOPER_API.md (V69)*

