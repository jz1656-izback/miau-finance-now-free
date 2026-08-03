# 🐱 Miau Finance API Reference

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "APIs are like cat doors —
               they work best when properly documented."
```

**Base URL**: `http://localhost:8000/api/v1`

**Version**: 0.8.0 | **Protocol**: REST + WebSocket

---

## Authentication

All API endpoints (except health) require a JWT Bearer token:

```
Authorization: Bearer <token>
```

Obtain a token via:

### `POST /api/v1/auth/token`

Request body:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Error Response Format

```json
{
  "detail": "Error description message"
}
```

Status codes: `200` Success, `400` Bad Request, `401` Unauthorized, `404` Not Found, `422` Validation Error, `429` Rate Limited, `500` Server Error.

---

## Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per authenticated user
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## Endpoints

---

### 🔷 Platform

#### `GET /api/v1/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "app": "Miau Finance"
}
```

#### `GET /api/v1`

API map listing all available endpoints.

**Response:**
```json
{
  "app": "Miau Finance",
  "version": "0.8.0",
  "endpoints": {
    "health": "GET /api/v1/health",
    "ontology_types": "GET /api/v1/ontology/types",
    ...
  }
}
```

---

### 🔷 Authentication

#### `POST /api/v1/auth/token`

Login to obtain a JWT access token.

| Parameter | Type | Description |
|---|---|---|
| `username` | string (body) | Your username |
| `password` | string (body) | Your password |

**Response:** `200`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Error:** `401` — Incorrect username or password.

---

### 🔷 Ontology

#### `GET /api/v1/ontology/types`

List all ontology object types.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `namespace` | string | — | Filter by namespace |

**Response:** `200`
```json
[
  {
    "id": "uuid",
    "name": "Instrument",
    "display_name": "Instrument",
    "description": "Financial instrument",
    "icon": "chart-bar",
    "color": "#00ff88"
  }
]
```

#### `GET /api/v1/ontology/types/{type_id}`

Get a single type with its properties and links.

| Parameter | Type | Description |
|---|---|---|
| `type_id` | UUID (path) | Type ID |

**Response:** `200`
```json
{
  "id": "uuid",
  "name": "Instrument",
  "display_name": "Instrument",
  "properties": [...],
  "links": [...]
}
```

#### `GET /api/v1/ontology/types/{type_id}/properties`

List properties for a type.

| Parameter | Type | Description |
|---|---|---|
| `type_id` | UUID (path) | Type ID |

#### `GET /api/v1/ontology/objects`

List/browse ontology objects.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type_id` | UUID | — | Filter by type |
| `search` | string | — | Full-text search |
| `status` | string | — | Filter by status |
| `tags` | string | — | Comma-separated tags |
| `limit` | int | 100 | Max results |
| `offset` | int | 0 | Pagination offset |

**Response:** `200`
```json
[
  {
    "id": "uuid",
    "display_name": "AAPL",
    "type_name": "Instrument",
    "status": "active",
    "properties": {}
  }
]
```

#### `GET /api/v1/ontology/objects/{object_id}`

Get a single object with its links.

| Parameter | Type | Description |
|---|---|---|
| `object_id` | UUID (path) | Object ID |

#### `GET /api/v1/ontology/objects/{object_id}/links`

Get links for a specific object.

#### `POST /api/v1/ontology/objects`

Create a new ontology object.

**Request body:**
```json
{
  "type_id": "uuid",
  "display_name": "AAPL",
  "description": "Apple Inc.",
  "status": "active",
  "tags": ["tech", "large-cap"],
  "properties": {"ticker": "AAPL", "sector": "Technology"},
  "created_by": "system"
}
```

#### `PUT /api/v1/ontology/objects/{object_id}`

Update an existing object.

**Request body:** (partial update)
```json
{
  "display_name": "Apple Inc.",
  "properties": {"ticker": "AAPL", "market_cap": 2800000000000}
}
```

#### `GET /api/v1/ontology/links`

List link definitions.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type_id` | UUID | — | Filter by source type |

#### `POST /api/v1/ontology/links`

Create a link between two objects.

**Request body:**
```json
{
  "link_id": "uuid",
  "source_object_id": "uuid",
  "target_object_id": "uuid",
  "properties": {}
}
```

---

### 🔷 Instruments

#### `GET /api/v1/instruments`

List financial instruments.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | — | Instrument type (stock, etf, bond, etc.) |
| `sector` | string | — | Sector filter |
| `exchange` | string | — | Exchange filter |
| `search` | string | — | Search by ticker, name, or ISIN |
| `limit` | int | 100 | Max results |
| `offset` | int | 0 | Pagination offset |

**Response:** `200`
```json
[
  {
    "id": "uuid",
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "instrument_type": "stock",
    "sector": "Technology",
    "exchange": "NASDAQ",
    "currency": "USD",
    "isin": "US0378331005"
  }
]
```

#### `GET /api/v1/instruments/{instrument_id}`

Get instrument detail.

| Parameter | Type | Description |
|---|---|---|
| `instrument_id` | UUID (path) | Instrument ID |

#### `GET /api/v1/instruments/{instrument_id}/market-data`

Get price history for an instrument.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `instrument_id` | UUID (path) | — | Instrument ID |
| `from_date` | string (date) | — | Start date (YYYY-MM-DD) |
| `to_date` | string (date) | — | End date (YYYY-MM-DD) |
| `limit` | int | 500 | Max records |

**Response:** `200`
```json
[
  {
    "date": "2024-01-15",
    "open": 185.5,
    "high": 187.2,
    "low": 184.8,
    "close": 186.9,
    "volume": 45000000
  }
]
```

#### `GET /api/v1/instruments/sectors/list`

List distinct sectors.

**Response:** `200`
```json
["Technology", "Healthcare", "Finance", "Energy"]
```

#### `GET /api/v1/instruments/types/list`

List distinct instrument types.

**Response:** `200`
```json
["stock", "etf", "mutual_fund", "bond", "crypto"]
```

---

### 🔷 Portfolios

#### `GET /api/v1/portfolios`

List all portfolios with summary metrics.

**Response:** `200`
```json
[
  {
    "id": "uuid",
    "name": "Tech Growth Fund",
    "portfolio_type": "growth",
    "base_currency": "USD",
    "management_style": "active",
    "status": "active",
    "num_positions": 15,
    "total_value": 2500000.00
  }
]
```

#### `GET /api/v1/portfolios/{portfolio_id}`

Get portfolio detail with positions.

| Parameter | Type | Description |
|---|---|---|
| `portfolio_id` | UUID (path) | Portfolio ID |

**Response:** `200`
```json
{
  "id": "uuid",
  "name": "Tech Growth Fund",
  "positions": [
    {
      "instrument_id": "uuid",
      "ticker": "AAPL",
      "quantity": 1000,
      "avg_price": 175.50,
      "market_value": 186900.00,
      "unrealized_pnl": 11400.00,
      "instrument_name": "Apple Inc."
    }
  ]
}
```

#### `GET /api/v1/portfolios/{portfolio_id}/positions`

Get position breakdown for a portfolio.

| Parameter | Type | Description |
|---|---|---|
| `portfolio_id` | UUID (path) | Portfolio ID |

**Response:** `200`
```json
[
  {
    "instrument_id": "uuid",
    "ticker": "AAPL",
    "quantity": 1000,
    "avg_price": 175.50,
    "market_value": 186900.00,
    "unrealized_pnl": 11400.00,
    "instrument_type": "stock",
    "sector": "Technology"
  }
]
```

#### `GET /api/v1/portfolios/{portfolio_id}/trades`

Get trades for a portfolio.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `portfolio_id` | UUID (path) | — | Portfolio ID |
| `limit` | int | 100 | Max results |

---

### 🔷 Trades

#### `GET /api/v1/trades`

List trades with filters.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `status` | string | — | Filter by status (executed, pending, cancelled) |
| `portfolio_id` | UUID | — | Filter by portfolio |
| `instrument_id` | UUID | — | Filter by instrument |
| `trader` | string | — | Filter by trader name |
| `limit` | int | 100 | Max results |
| `offset` | int | 0 | Pagination offset |

**Response:** `200`
```json
[
  {
    "id": "uuid",
    "ticker": "AAPL",
    "side": "buy",
    "quantity": 500,
    "price": 185.00,
    "notional": 92500.00,
    "trade_date": "2024-01-15T10:30:00Z",
    "status": "executed",
    "trader": "miau_trader",
    "instrument_name": "Apple Inc.",
    "portfolio_name": "Tech Growth Fund"
  }
]
```

#### `GET /api/v1/trades/{trade_id}`

Get trade detail with counterparty info.

| Parameter | Type | Description |
|---|---|---|
| `trade_id` | UUID (path) | Trade ID |

---

### 🔷 Search

#### `GET /api/v1/search`

Full-text search across ontology objects.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string (required) | — | Search query |
| `type` | string | — | Filter by object type |
| `limit` | int | 50 | Max results |

**Response:** `200`
```json
{
  "query": "Apple",
  "total": 3,
  "results": [
    {
      "id": "uuid",
      "display_name": "Apple Inc.",
      "type_name": "Instrument",
      "type_display_name": "Instrument"
    }
  ]
}
```

---

### 🔷 Pipelines

#### `GET /api/v1/pipelines/runs`

List pipeline execution runs.

**Response:** `200`
```json
[
  {
    "id": "uuid",
    "pipeline_name": "daily_market_data",
    "status": "completed",
    "started_at": "2024-01-15T00:00:00Z",
    "finished_at": "2024-01-15T00:05:30Z",
    "error_message": null
  }
]
```

#### `POST /api/v1/pipelines/runs`

Create a new manual pipeline run.

#### `POST /api/v1/pipelines/calculate/pnl`

Calculate P&L from current positions.

**Response:** `200`
```json
{
  "status": "ok",
  "message": "P&L calculated"
}
```

---

### 🔷 Analytics (Combined)

#### `GET /api/v1/analytics/summary`

Platform-wide summary dashboard.

**Response:** `200`
```json
{
  "total_portfolios": 3,
  "total_instruments": 1250,
  "total_trades": 5432,
  "total_aum": 4300000.00,
  "total_unrealized_pnl": 125000.00
}
```

#### `GET /api/v1/analytics/portfolios/{portfolio_id}`

Portfolio analytics with summary, P&L, and risk.

| Parameter | Type | Description |
|---|---|---|
| `portfolio_id` | UUID (path) | Portfolio ID |

**Response:** `200`
```json
{
  "summary": { ... },
  "pnl_timeseries": [ ... ],
  "risk_metrics": [ ... ]
}
```

#### `GET /api/v1/analytics/instruments/{instrument_id}/performance`

Instrument performance metrics.

| Parameter | Type | Description |
|---|---|---|
| `instrument_id` | UUID (path) | Instrument ID |

#### `GET /api/v1/analytics/pnl/timeseries`

P&L time series.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `portfolio_id` | UUID | — | Optional portfolio filter |
| `days` | int | 30 | Number of days |

**Response:** `200`
```json
[
  {
    "date": "2024-01-15",
    "pnl": 12500.00,
    "pnl_pct": 2.5
  }
]
```

#### `GET /api/v1/analytics/portfolios/{portfolio_id}/risk`

Portfolio risk metrics.

| Parameter | Type | Description |
|---|---|---|
| `portfolio_id` | UUID (path) | Portfolio ID |

---

### 🔷 Market Data

#### `GET /api/v1/market/live`

Real-time live prices.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL,AMZN,TSLA,SPY,QQQ` | Comma-separated tickers |

**Response:** `200`
```json
{
  "data": {
    "AAPL": {
      "price": 186.90,
      "change_pct": 1.25,
      "high": 187.50,
      "low": 185.20,
      "volume": 45200000,
      "name": "Apple Inc."
    }
  }
}
```

#### `GET /api/v1/market/historical/{ticker}`

Historical price data.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string (path) | — | Ticker symbol |
| `period` | string | `6mo` | Period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, ytd, max) |
| `interval` | string | `1d` | Interval (1m, 5m, 15m, 1h, 1d, 1wk, 1mo) |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "period": "6mo",
  "records": [
    {
      "date": "2024-01-15",
      "open": 185.50,
      "high": 187.20,
      "low": 184.80,
      "close": 186.90,
      "volume": 45000000
    }
  ]
}
```

#### `GET /api/v1/market/movers`

Top market gainers and losers.

**Response:** `200` — Array of movers with ticker, name, price, and change_pct.

#### `GET /api/v1/market/sectors`

Sector performance data.

**Response:** `200`
```json
[
  {
    "ticker": "XLK",
    "name": "Technology Select Sector SPDR Fund",
    "price": 215.50,
    "change_pct": 1.82
  }
]
```

#### `GET /api/v1/market/indicators`

US market indicators.

**Response:** `200`
```json
{
  "gdp": "2.5%",
  "unemployment": "3.7%",
  "cpi": "3.1%",
  "fed_rate": "5.25-5.50%"
}
```

#### `GET /api/v1/market/crypto`

Single cryptocurrency price.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `coin` | string | `bitcoin` | Coin name (bitcoin, ethereum, etc.) |

**Response:** `200`
```json
{
  "symbol": "BTC",
  "price": 43250.00,
  "change_24h_pct": 2.35,
  "market_cap": 848000000000,
  "volume_24h": 28000000000
}
```

#### `GET /api/v1/market/crypto/top`

Top cryptocurrencies by market cap.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | int | 20 | Number of coins |

**Response:** `200`
```json
[
  {
    "rank": 1,
    "symbol": "BTC",
    "name": "Bitcoin",
    "price": 43250.00,
    "change_24h_pct": 2.35,
    "market_cap": 848000000000
  }
]
```

#### `GET /api/v1/market/crypto/market`

Crypto market overview.

**Response:** `200`
```json
{
  "total_market_cap_trillions": 1.75,
  "total_volume_24h_trillions": 0.085,
  "btc_dominance_pct": 48.5,
  "active_cryptos": 12500,
  "markets": 850
}
```

#### `GET /api/v1/market/crypto/fear-greed`

Fear & Greed index.

**Response:** `200`
```json
{
  "value": 65,
  "classification": "Greed",
  "timestamp": "2024-01-15T00:00:00Z"
}
```

#### `GET /api/v1/market/crypto/historical`

Cryptocurrency historical prices.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `coin` | string | `bitcoin` | Coin name |
| `days` | int | 30 | Number of days |

**Response:** `200`
```json
{
  "coin": "bitcoin",
  "prices": [
    { "date": "2024-01-15", "price": 43250.00 },
    { "date": "2024-01-14", "price": 42800.00 }
  ]
}
```

#### `GET /api/v1/market/forex`

Forex exchange rates.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `base` | string | `USD` | Base currency |
| `targets` | string | — | Comma-separated targets (e.g., EUR,GBP,JPY) |

**Response:** `200`
```json
{
  "base": "USD",
  "rates": {
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 149.50,
    "CHF": 0.87
  }
}
```

---

### 🔷 Currencies

Multi-currency support: list supported currencies, convert between them, and manage portfolio base currency.

#### `GET /api/v1/currencies`

List all supported currencies with metadata.

**Response:** `200`
```json
{
  "USD": {"symbol": "$", "decimals": 2, "name": "US Dollar"},
  "EUR": {"symbol": "€", "decimals": 2, "name": "Euro"},
  "JPY": {"symbol": "¥", "decimals": 0, "name": "Japanese Yen"},
  "GBP": {"symbol": "£", "decimals": 2, "name": "British Pound"},
  "BRL": {"symbol": "R$", "decimals": 2, "name": "Brazilian Real"},
  "INR": {"symbol": "₹", "decimals": 2, "name": "Indian Rupee"}
}
```

#### `GET /api/v1/currencies/convert`

Convert an amount between currencies using live FX rates.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `amount` | float | — | Amount to convert |
| `from` | string | `USD` | Source currency code |
| `to` | string | `EUR` | Target currency code |

**Response:** `200`
```json
{
  "from": "USD",
  "to": "EUR",
  "amount": 100.00,
  "result": 92.50,
  "rate": 0.925,
  "timestamp": "2026-05-19T12:00:00Z"
}
```

#### `PUT /api/v1/portfolios/{portfolio_id}/currency`

Change the base currency of an existing portfolio.

| Parameter | Type | Description |
|---|---|---|
| `portfolio_id` | UUID (path) | Portfolio ID |

**Request body:**
```json
{
  "currency": "EUR"
}
```

**Response:** `200`
```json
{
  "id": "uuid",
  "name": "Tech Growth Fund",
  "base_currency": "EUR",
  "status": "updated"
}
```

---

### 🔷 News

#### `GET /api/v1/news/market`

Market news feed.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | — | Optional ticker filter |
| `limit` | int | 10 | Max articles |

**Response:** `200`
```json
[
  {
    "title": "Apple Reports Record Quarterly Revenue",
    "publisher": "Financial Times",
    "published_at": "2024-01-15T14:30:00Z",
    "summary": "Apple Inc. reported...",
    "url": "https://..."
  }
]
```

#### `GET /api/v1/news/company/{ticker}`

Company-specific news.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string (path) | — | Ticker symbol |
| `limit` | int | 10 | Max articles |

#### `GET /api/v1/news/batch`

Batch news for multiple tickers.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL,AMZN,TSLA` | Comma-separated tickers |
| `limit` | int | 5 | Articles per ticker |

---

### 🔷 Sentiment Analysis

#### `GET /api/v1/sentiment/sentiment`

Analyze news sentiment for a single ticker.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | `AAPL` | Ticker symbol |
| `days` | int | 7 | Lookback days (1–365) |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "average_sentiment": 0.35,
  "sentiment_label": "positive",
  "articles_analyzed": 42,
  "positive_count": 28,
  "negative_count": 10,
  "neutral_count": 4
}
```

#### `GET /api/v1/sentiment/sentiment/market`

Analyze overall market sentiment.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `days` | int | 1 | Lookback days (1–30) |

**Response:** `200`
```json
{
  "average_sentiment": 0.12,
  "sentiment_label": "neutral",
  "articles_analyzed": 156
}
```

---

### 🔷 Portfolio Optimizer

#### `GET /api/v1/optimizer/optimize`

Maximize Sharpe ratio portfolio.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL` | Comma-separated tickers |
| `risk_free` | float | 0.05 | Risk-free rate |
| `period` | string | `1y` | Lookback period |

**Response:** `200`
```json
{
  "expected_return": 0.1523,
  "expected_volatility": 0.1821,
  "sharpe_ratio": 0.84,
  "weights": {
    "AAPL": 0.35,
    "MSFT": 0.40,
    "GOOGL": 0.25
  }
}
```

#### `GET /api/v1/optimizer/min-variance`

Minimum variance portfolio.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL` | Comma-separated tickers |
| `period` | string | `1y` | Lookback period |

**Response:** `200` — Same format as optimize.

#### `GET /api/v1/optimizer/equal-weight`

Equal weight portfolio.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL` | Comma-separated tickers |
| `period` | string | `1y` | Lookback period |

#### `GET /api/v1/optimizer/performance`

Performance metrics for assets.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL` | Comma-separated tickers |
| `period` | string | `1y` | Lookback period |
| `risk_free` | float | 0.05 | Risk-free rate |

**Response:** `200`
```json
{
  "AAPL": {
    "sharpe_ratio": 1.25,
    "sortino_ratio": 1.85,
    "annualized_return": 18.5,
    "annualized_volatility": 15.2,
    "max_drawdown_pct": -12.3
  }
}
```

#### `POST /api/v1/optimizer/black-litterman`

Black-Litterman portfolio optimization with investor views.

**Request body:**
```json
{
  "tickers": ["AAPL", "MSFT", "GOOGL"],
  "market_cap_weights": [0.35, 0.40, 0.25],
  "views": [
    {
      "ticker": "AAPL",
      "view_type": "absolute",
      "q": 0.20,
      "confidence": 0.5
    }
  ],
  "risk_aversion": 2.5
}
```

**Response:** `200`
```json
{
  "expected_return": 0.1423,
  "expected_volatility": 0.1721,
  "sharpe_ratio": 0.87,
  "weights": {
    "AAPL": 0.38,
    "MSFT": 0.38,
    "GOOGL": 0.24
  }
}
```

---

### 🔷 Risk Analytics

#### `GET /api/v1/risk/var`

Value at Risk calculation.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | `SPY` | Ticker symbol |
| `confidence` | float | 0.95 | Confidence level |
| `method` | string | `historical` | Method (historical, parametric, monte_carlo) |
| `period` | string | `2y` | Lookback period |

**Response:** `200`
```json
{
  "ticker": "SPY",
  "confidence": 0.95,
  "var": -0.0215,
  "cvar": -0.0318,
  "var_1_month": -0.0923
}
```

#### `GET /api/v1/risk/beta`

Beta calculation vs benchmark.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | `AAPL` | Ticker symbol |
| `benchmark` | string | `SPY` | Benchmark ticker |
| `period` | string | `2y` | Lookback period |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "benchmark": "SPY",
  "beta": 1.25,
  "alpha": 0.0015,
  "correlation": 0.82,
  "r_squared": 0.67
}
```

#### `GET /api/v1/risk/stress-test`

Stress test scenarios.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | `SPY` | Ticker symbol |
| `period` | string | `2y` | Lookback period |

**Response:** `200`
```json
{
  "2008_financial_crisis": {
    "description": "2008 Financial Crisis (-37%)",
    "impact": -0.372,
    "impact_label": "-37.2%"
  },
  "covid_crash": {
    "description": "COVID-19 Crash (-34%)",
    "impact": -0.341,
    "impact_label": "-34.1%"
  },
  "rate_hike": {
    "description": "Rate Hike Shock (-15%)",
    "impact": -0.150,
    "impact_label": "-15.0%"
  }
}
```

#### `GET /api/v1/risk/greeks`

Options Greeks calculator.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `spot` | float | 100 | Spot price |
| `strike` | float | 105 | Strike price |
| `days_to_expiry` | float | 30 | Days to expiration |
| `risk_free` | float | 0.05 | Risk-free rate |
| `volatility` | float | 0.25 | Implied volatility |
| `option_type` | string | `call` | Option type (call/put) |

**Response:** `200`
```json
{
  "option_type": "call",
  "price": 3.25,
  "delta": 0.4521,
  "gamma": 0.0321,
  "theta": -0.0521,
  "vega": 0.0821,
  "rho": 0.0121
}
```

#### `GET /api/v1/risk/comprehensive`

Comprehensive risk report.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | `AAPL` | Ticker symbol |
| `period` | string | `2y` | Lookback period |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "var_95": {
    "var": -0.0215,
    "cvar": -0.0318,
    "var_1_month": -0.0923
  },
  "var_99": {
    "var": -0.0358,
    "cvar": -0.0482,
    "var_1_month": -0.1250
  },
  "beta": {
    "beta": 1.25,
    "alpha": 0.0015,
    "correlation": 0.82,
    "r_squared": 0.67
  },
  "stress_test": {
    "2008_financial_crisis": { "impact": -0.372, "impact_label": "-37.2%" }
  }
}
```

---

### 🔷 Trading Signals

#### `GET /api/v1/signals/generate`

Generate technical trading signals.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | `AAPL` | Ticker symbol |
| `period` | string | `6mo` | Lookback period |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "price": 186.90,
  "trend": "bullish",
  "indicators": {
    "sma_20": 184.50,
    "sma_50": 180.20,
    "rsi_14": 62.5,
    "macd": 1.25
  },
  "signals": [
    {
      "type": "BUY",
      "strength": "medium",
      "indicator": "MACD",
      "detail": "MACD crossed above signal line"
    }
  ]
}
```

#### `GET /api/v1/signals/multi`

Multi-asset signals.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL,AMZN,TSLA` | Comma-separated tickers |
| `period` | string | `3mo` | Lookback period |

#### `GET /api/v1/signals/backtest`

Backtest a trading strategy.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | `AAPL` | Ticker symbol |
| `strategy` | string | `sma_cross` | Strategy (sma_cross) |
| `short_window` | int | 20 | Short SMA window |
| `long_window` | int | 50 | Long SMA window |
| `initial_capital` | float | 100000 | Starting capital |
| `period` | string | `2y` | Backtest period |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "strategy": "sma_cross",
  "total_return_pct": 18.5,
  "buy_and_hold_return_pct": 15.2,
  "outperformance_pct": 3.3,
  "sharpe_ratio": 1.25,
  "max_drawdown_pct": -8.5,
  "win_rate_pct": 55.0,
  "num_trades": 12,
  "final_capital": 118500.00
}
```

---

### 🔷 Fundamentals

#### `GET /api/v1/fundamentals/{ticker}`

Company overview and financials.

| Parameter | Type | Description |
|---|---|---|
| `ticker` | string (path) | Ticker symbol |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "employees": 164000,
  "description": "Apple Inc. designs, manufactures, and markets smartphones...",
  "valuation": {
    "market_cap": 2800000000000,
    "pe_ratio": 28.5,
    "forward_pe": 25.2,
    "price_to_book": 45.0,
    "price_to_sales": 7.8,
    "enterprise_to_ebitda": 22.5
  },
  "price_targets": {
    "target_mean": 200.00,
    "target_high": 250.00,
    "target_low": 165.00,
    "recommendation": "Buy"
  }
}
```

#### `GET /api/v1/fundamentals/{ticker}/earnings`

Earnings calendar.

| Parameter | Type | Description |
|---|---|---|
| `ticker` | string (path) | Ticker symbol |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "earnings": [
    {
      "date": "2024-01-30",
      "eps_estimate": 2.10,
      "eps_actual": 2.18
    }
  ]
}
```

#### `GET /api/v1/fundamentals/{ticker}/filings`

SEC EDGAR filings (10-K, 10-Q, 8-K).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string (path) | — | Ticker symbol |
| `filing_types` | string | — | Comma-separated types (10-K,10-Q,8-K) |
| `limit` | int | 20 | Max filings |

**Response:** `200`
```json
[
  {
    "filing_date": "2024-01-30",
    "form": "10-Q",
    "accession_number": "0000320193-24-000010",
    "primary_doc_url": "https://www.sec.gov/Archives/...",
    "description": "Quarterly report"
  }
]
```

#### `GET /api/v1/fundamentals/{ticker}/insider-trades`

Insider trading activity (Form 4).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string (path) | — | Ticker symbol |
| `limit` | int | 50 | Max transactions |

**Response:** `200`
```json
[
  {
    "filing_date": "2024-01-15",
    "insider_name": "Tim Cook",
    "title": "Chief Executive Officer",
    "transaction_type": "Sale",
    "shares": 50000,
    "price": 185.50,
    "value": 9275000
  }
]
```

---

### 🔷 Economics

#### `GET /api/v1/economics/commodities`

Commodity prices.

**Response:** `200`
```json
{
  "Gold": { "price": 2050.50, "change_pct": 0.85 },
  "Silver": { "price": 24.50, "change_pct": -0.25 },
  "Crude Oil": { "price": 78.30, "change_pct": 1.50 },
  "Copper": { "price": 3.85, "change_pct": 0.45 },
  "Natural Gas": { "price": 2.45, "change_pct": -1.20 }
}
```

#### `GET /api/v1/economics/treasury-yield`

US Treasury yields.

**Response:** `200`
```json
{
  "2y": { "yield": 4.35, "change": 0.02 },
  "5y": { "yield": 4.12, "change": -0.01 },
  "10y": { "yield": 4.08, "change": 0.03 },
  "30y": { "yield": 4.25, "change": 0.01 }
}
```

#### `GET /api/v1/economics/market-breadth`

Market breadth indices.

**Response:** `200`
```json
{
  "S&P 500": { "value": 4850.50, "change_pct": 0.75 },
  "NASDAQ": { "value": 15250.00, "change_pct": 1.25 },
  "DOW": { "value": 38250.00, "change_pct": 0.45 },
  "RUSSELL 2000": { "value": 2050.00, "change_pct": 1.10 },
  "VIX": { "value": 13.50, "change_pct": -2.50 }
}
```

#### `GET /api/v1/economics/gainers-losers`

Top gainers and losers.

**Response:** `200`
```json
{
  "top_gainers": [
    { "ticker": "NVDA", "name": "NVIDIA Corporation", "change_pct": 5.25, "price": 685.50 }
  ],
  "top_losers": [
    { "ticker": "INTC", "name": "Intel Corporation", "change_pct": -3.50, "price": 45.20 }
  ]
}
```

#### `GET /api/v1/economics/correlation`

Asset correlation matrix.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL,AMZN,TSLA` | Comma-separated tickers |

**Response:** `200`
```json
{
  "tickers": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
  "correlation_matrix": {
    "AAPL": { "AAPL": 1.0, "MSFT": 0.82, "GOOGL": 0.75, "AMZN": 0.78, "TSLA": 0.45 },
    "MSFT": { "AAPL": 0.82, "MSFT": 1.0, "GOOGL": 0.79, "AMZN": 0.72, "TSLA": 0.42 }
  },
  "as_of": "2024-01-15T00:00:00"
}
```

#### `GET /api/v1/economics/fred`

FRED economic indicators (GDP, CPI, unemployment, etc.).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `series_ids` | string | `GDP,CPIAUCSL,UNRATE,FEDFUNDS,DGS10,DGS2` | Comma-separated FRED series IDs |
| `limit` | int | 100 | Max observations per series |

**Response:** `200`
```json
{
  "GDP": {
    "series_id": "GDP",
    "title": "Gross Domestic Product",
    "observations": [
      { "date": "2024-01-01", "value": 27939.1 }
    ]
  },
  "CPIAUCSL": {
    "series_id": "CPIAUCSL",
    "title": "Consumer Price Index",
    "observations": [
      { "date": "2024-01-01", "value": 308.417 }
    ]
  }
}
```

---

### 🔷 Watchlist

#### `GET /api/v1/watchlist`

List user's watchlists.

**Response:** `200`
```json
{
  "watchlists": [
    { "id": "uuid", "name": "Default", "created_at": "2025-01-15T12:00:00", "item_count": 5 }
  ]
}
```

#### `POST /api/v1/watchlist`

Create a new watchlist.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | string | `Default` | Watchlist name |

**Response:** `200`
```json
{ "id": "uuid", "name": "My Watchlist" }
```

#### `GET /api/v1/watchlist/items`

List all watchlist items.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `watchlist_id` | string | — | Optional: filter by watchlist |

**Response:** `200`
```json
{
  "items": [
    { "id": "uuid", "ticker": "AAPL", "added_at": "2025-01-15T12:00:00", "notes": "" }
  ]
}
```

#### `POST /api/v1/watchlist/items`

Add a ticker to the watchlist (auto-creates default watchlist if needed).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | — | Ticker symbol (1-10 chars) |
| `notes` | string | — | Optional notes |
| `watchlist_id` | string | — | Optional: target watchlist |

**Response:** `200`
```json
{ "id": "uuid", "ticker": "AAPL", "added_at": "2025-01-15T12:00:00", "message": "Added AAPL to watchlist" }
```

**Error `409`:** `{"detail": "AAPL already in watchlist"}`

#### `DELETE /api/v1/watchlist/items`

Remove a ticker from the watchlist.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | — | Ticker to remove |
| `watchlist_id` | string | — | Optional: target watchlist |

**Response:** `200`
```json
{ "message": "Removed AAPL from watchlist" }
```

**Error `404`:** `{"detail": "AAPL not found in watchlist"}`

---

### 🔷 Options Chain

#### `GET /api/v1/options/{ticker}`

Full options chain for a ticker.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string (path) | — | Ticker symbol |
| `expiration` | string | — | Unix timestamp for specific expiration |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "underlying_price": 186.90,
  "expiration_dates": ["2024-02-16", "2024-03-15"],
  "calls": [
    {
      "strike": 185.0,
      "last_price": 5.20,
      "bid": 5.10,
      "ask": 5.30,
      "volume": 1250,
      "open_interest": 5432,
      "implied_volatility": 0.28
    }
  ],
  "puts": [
    {
      "strike": 185.0,
      "last_price": 3.10,
      "bid": 3.00,
      "ask": 3.20,
      "volume": 890,
      "open_interest": 3210,
      "implied_volatility": 0.29
    }
  ]
}
```

---

### 🔷 Global Markets

Unified global market data across 40 international exchanges in Asia, Europe, Latin America, and Middle East/Africa.

#### `GET /api/v1/markets/global`

Get benchmark indices and prices for all supported global exchanges.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `region` | string | — | Optional filter: `asia`, `europe`, `latam`, `mea` |

**Response:** `200`
```json
[
  {
    "code": "TSE",
    "name": "Tokyo Stock Exchange",
    "country": "Japan",
    "benchmark": "^N225",
    "price": 38500.00,
    "change_pct": 1.25,
    "currency": "JPY"
  },
  {
    "code": "LSE",
    "name": "London Stock Exchange",
    "country": "United Kingdom",
    "benchmark": "^FTSE",
    "price": 8250.00,
    "change_pct": -0.30,
    "currency": "GBP"
  }
]
```

#### `GET /api/v1/markets/global/{exchange}`

Get detailed data for a specific exchange, including marker stock prices and index history.

| Parameter | Type | Description |
|---|---|---|
| `exchange` | string (path) | Exchange code (e.g. `TSE`, `LSE`, `B3`, `TADAWUL`) |

**Response:** `200`
```json
{
  "code": "TSE",
  "name": "Tokyo Stock Exchange",
  "country": "Japan",
  "benchmark": "^N225",
  "price": 38500.00,
  "change_pct": 1.25,
  "currency": "JPY",
  "market_hours": {
    "open": "09:00",
    "close": "15:00",
    "timezone": "Asia/Tokyo",
    "is_open": true
  },
  "stocks": [
    {"symbol": "7203.T", "price": 3200.00, "change_pct": 0.80},
    {"symbol": "9984.T", "price": 12500.00, "change_pct": -0.50}
  ]
}
```

---

### 🔷 Monte Carlo Simulation

#### `GET /api/v1/analytics/monte-carlo`

Run Monte Carlo price simulation.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string | `AAPL` | Ticker symbol |
| `num_simulations` | int | 1000 | Number of paths (100–100000) |
| `days` | int | 252 | Simulation horizon (10–2520) |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "current_price": 186.90,
  "num_simulations": 1000,
  "days": 252,
  "statistics": {
    "mean_final_price": 195.40,
    "median_final_price": 194.20,
    "std_dev": 28.50,
    "min_price": 125.30,
    "max_price": 310.80,
    "prob_profit": 0.62,
    "prob_10pct_loss": 0.18,
    "prob_20pct_loss": 0.08
  },
  "percentiles": {
    "p5": 148.20,
    "p10": 158.40,
    "p25": 175.60,
    "p50": 194.20,
    "p75": 213.80,
    "p90": 234.50,
    "p95": 248.90
  }
}
```

---

### 🔷 Pairs Trading

#### `GET /api/v1/analytics/pairs/find`

Find cointegrated pairs from a list of tickers.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `tickers` | string | `AAPL,MSFT,GOOGL,AMZN,TSLA` | Comma-separated tickers |
| `confidence` | float | `0.95` | ADF test confidence level |

**Response:** `200`
```json
{
  "pairs": [
    {
      "ticker1": "AAPL",
      "ticker2": "MSFT",
      "adf_statistic": -3.42,
      "p_value": 0.008,
      "half_life": 15.3,
      "hedge_ratio": 0.82,
      "z_score": -1.85,
      "signal": "long_short"
    }
  ],
  "total_pairs": 1
}
```

#### `GET /api/v1/analytics/pairs/backtest`

Backtest a pairs trading strategy.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker1` | string | `AAPL` | First ticker |
| `ticker2` | string | `MSFT` | Second ticker |
| `entry_z` | float | `2.0` | Z-score entry threshold |
| `exit_z` | float | `0.5` | Z-score exit threshold |

**Response:** `200`
```json
{
  "ticker1": "AAPL",
  "ticker2": "MSFT",
  "total_trades": 12,
  "win_rate": 0.75,
  "total_return_pct": 8.45,
  "sharpe": 1.82,
  "max_drawdown_pct": -3.20
}
```

---

### 🔷 Reports

#### `GET /api/v1/reports/portfolio/{portfolio_id}`

Download portfolio PDF report.

| Parameter | Type | Description |
|---|---|---|
| `portfolio_id` | UUID (path) | Portfolio ID |

**Response:** `200` — PDF file download (`Content-Type: application/pdf`)

#### `GET /api/v1/reports/portfolio/{portfolio_id}/excel`

Download portfolio positions as Excel spreadsheet.

| Parameter | Type | Description |
|---|---|---|
| `portfolio_id` | UUID (path) | Portfolio ID |

**Response:** `200` — XLSX file download (`Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`)

#### `GET /api/v1/reports/trades/csv`

Download all trades as CSV.

**Response:** `200` — CSV file download (`Content-Type: text/csv`)

---

### 🔷 WebSocket

#### `WS /api/v1/ws/prices`

Real-time price streaming via WebSocket.

**Connection:** Establish WebSocket to `ws://localhost:8000/api/v1/ws/prices`

**Send (subscribe):**
```json
{
  "tickers": ["AAPL", "MSFT", "GOOGL", "TSLA"]
}
```

**Receive (every 2 seconds):**
```json
{
  "ticker": "AAPL",
  "price": 187.25,
  "change_pct": 1.35,
  "timestamp": "2024-01-15T14:30:00.123Z"
}
```

---

### 🔷 AI Advisor

#### `POST /api/v1/ai/advisor/portfolio`

AI-powered portfolio analysis with personalized recommendations.

**Request body:**
```json
{
  "portfolio_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:** `200`
```json
{
  "summary": "Portfolio is well-diversified with moderate risk exposure...",
  "strengths": ["Strong tech sector allocation", "Low correlation between holdings"],
  "weaknesses": ["Overweight in growth stocks", "Limited international exposure"],
  "recommendations": ["Consider adding fixed income", "Reduce TSLA position by 5%"],
  "risk_level": "medium"
}
```

**Error `500`:** `{"detail": "Analysis failed"}`

#### `POST /api/v1/ai/advisor/market`

AI-powered market overview analysis.

**Request body:** `{}`

**Response:** `200`
```json
{
  "market_sentiment": "cautiously bullish",
  "hot_sectors": ["Technology", "Healthcare"],
  "key_risks": ["Rate hike uncertainty", "Geopolitical tensions"],
  "recommendations": ["Focus on quality large caps", "Defensive positioning"]
}
```

#### `POST /api/v1/ai/advisor/risk`

AI-powered risk assessment for a portfolio.

**Request body:**
```json
{
  "portfolio_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:** `200`
```json
{
  "summary": "Portfolio has moderate risk with concentration in tech",
  "risk_level": "medium",
  "risk_factors": ["Sector concentration", "Growth stock volatility"],
  "mitigations": ["Sector diversification", "Add hedging strategies"]
}
```

#### `POST /api/v1/ai/query`

General AI query for financial questions.

**Request body:**
```json
{
  "query": "What is the current price of AAPL?"
}
```

**Response:** `200`
```json
{
  "response": "Apple (AAPL) is currently trading at $150.25..."
}
```

**Error `503`:** `{"detail": "AI not configured"}` — returned when `AI_API_KEY` is not set.

---

### 🔷 DeFi & Web3

WalletConnect, DeFi protocol data, NFT portfolio tracking, and cross-chain bridging.

#### Wallet

##### `GET /api/v1/defi/wallet/chains`

List supported blockchain networks.

**Response:** `200`
```json
{"chains": ["ethereum", "arbitrum", "optimism", "polygon", "base", "solana"]}
```

##### `POST /api/v1/defi/wallet/connect`

Initiate a WalletConnect v2 session. Returns a URI to scan with a wallet app.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `wallet_type` | string | `evm` | Wallet type: `evm`, `solana` |

**Response:** `200`
```json
{"message": "Scan the URI with your evm wallet to connect", "session": {"uri": "wc:..."}}
```

##### `GET /api/v1/defi/wallet/sessions`

List active wallet sessions.

##### `GET /api/v1/defi/wallet/sessions/{topic}`

Get session details by topic.

##### `POST /api/v1/defi/wallet/sessions/{topic}/disconnect`

Disconnect a wallet session.

##### `POST /api/v1/defi/wallet/sessions/{topic}/chain`

Switch blockchain network for a session.

| Parameter | Type | Description |
|---|---|---|
| `chain_id` | string | Target chain ID (e.g. `eip155:42161` for Arbitrum) |

##### `POST /api/v1/defi/wallet/balances`

Fetch aggregated balances across all connected wallets and chains.

**Response:** `200`
```json
{
  "balances": [
    {"chain": "ethereum", "asset": "ETH", "amount": 1.5, "usd_value": 4875.00},
    {"chain": "arbitrum", "asset": "USDC", "amount": 2500.0, "usd_value": 2500.00}
  ],
  "total_usd": 7375.00
}
```

#### DeFi Protocols

##### Uniswap

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/protocols/uniswap/pool?pool=0x...&chain=ethereum` | Uniswap v3 pool info (price, liquidity, fee, tokens) |
| `GET /api/v1/defi/protocols/uniswap/swap?token_in=WETH&token_out=USDC&amount=1.0` | Simulate a swap |

##### Aave

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/protocols/aave/reserve?asset=USDC` | Reserve data (deposit/borrow rates, LTV, liquidation) |
| `GET /api/v1/defi/protocols/aave/deposit?asset=USDC&amount=1000` | Simulate deposit with estimated yield |
| `GET /api/v1/defi/protocols/aave/borrow?asset=USDC&amount=1000` | Simulate borrow with interest estimates |

##### Curve Finance

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/protocols/curve/pools` | List all pools (3Pool, stETH, FRAX, TriCrypto) |
| `GET /api/v1/defi/protocols/curve/pool/{pool_id}` | Pool detail with tokens and APY |

##### Lido

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/protocols/lido/info` | Staking overview (APY, TVL, validators, node operators) |
| `GET /api/v1/defi/protocols/lido/stake?amount=10.0` | Simulate staking ETH for stETH |

##### Yearn Finance

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/protocols/yearn/vaults` | List all vaults with APY and strategy |
| `GET /api/v1/defi/protocols/yearn/vault/{vault_id}` | Vault detail |

##### MakerDAO

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/protocols/maker/vault-types` | List CDP vault types (ETH-A/B/C, WBTC-A, USDC-A, etc.) |
| `GET /api/v1/defi/protocols/maker/simulate?collateral=WETH&deposit=10000&draw=5000` | Simulate opening a vault |

##### Solana DeFi

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/protocols/solana/jupiter-pairs` | Jupiter aggregator pairs with price and volume |
| `GET /api/v1/defi/protocols/solana/jupiter-swap?sol_amount=1.0` | Simulate swap via Jupiter |
| `GET /api/v1/defi/protocols/solana/raydium-pools` | Raydium AMM pools with APY and TVL |
| `GET /api/v1/defi/protocols/solana/raydium-lp?pool=SOL-USDC&amount=10.0` | Simulate LP deposit |
| `GET /api/v1/defi/protocols/solana/marinade-info` | Marinade staking overview |
| `GET /api/v1/defi/protocols/solana/marinade-stake?amount=10.0` | Simulate staking SOL for mSOL |

##### Yield Aggregator

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/protocols/yield/all?min_apy=0&max_risk=high` | Best yields across all protocols |
| `GET /api/v1/defi/protocols/yield/best?asset=USDC` | Best yield for a specific asset |
| `GET /api/v1/defi/protocols/yield/protocol?name=Aave` | Protocol summary with all products |

##### Cross-Chain Bridges

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/bridges/list` | List all supported bridges |
| `GET /api/v1/defi/bridges/info?name=LayerZero` | Bridge detail |
| `GET /api/v1/defi/bridges/assets` | Supported assets per bridge |
| `GET /api/v1/defi/bridges/simulate?asset=USDC&amount=1000&from=ethereum&to=arbitrum&bridge=LayerZero` | Simulate a bridge transfer |

#### NFT Services

##### Portfolio

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/nft/portfolio?wallet=0x...` | NFT portfolio with cost basis, P&L, rarity |

##### Floor Price

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/nft/floor/{collection}` | Floor price, 24h change, volume |
| `GET /api/v1/defi/nft/collections` | All tracked collections |
| `GET /api/v1/defi/nft/alert?collection=azuki&threshold=4.5&direction=below` | Set floor price alert |
| `GET /api/v1/defi/nft/value?collection=bored-ape-yacht-club&token_id=1001&attributes=gold_fur,laser_eyes` | Estimate NFT value with trait bonuses |

##### Marketplace

| Endpoint | Description |
|---|---|
| `GET /api/v1/defi/nft/listings?collection=Bored%20Ape&sort=price_asc` | Browse marketplace listings |
| `GET /api/v1/defi/nft/listings/{listing_id}` | Listing detail |
| `GET /api/v1/defi/nft/buy?listing_id=listing_1` | Simulate purchase with fees |
| `GET /api/v1/defi/nft/marketplaces` | List supported marketplaces |

---

### 🔷 Natural Language Query (NLQ)

The system supports natural language queries that are parsed into structured API calls.

**Intent mapping:** The NLQ parser maps plain English queries to API endpoints. Supported intents:

| Intent | Example Query | API Endpoint |
|---|---|---|
| `price` | "What is AAPL price?" | `GET /api/v1/market/live` |
| `portfolio` | "Show my portfolios" | `GET /api/v1/portfolios` |
| `positions` | "What are my holdings?" | `GET /api/v1/portfolios/{id}/positions` |
| `news` | "Latest news" | `GET /api/v1/news/market` |
| `company_news` | "AAPL news" | `GET /api/v1/news/company/{ticker}` |
| `fundamentals` | "AAPL fundamentals" | `GET /api/v1/fundamentals/{ticker}` |
| `earnings` | "AAPL earnings" | `GET /api/v1/fundamentals/{ticker}/earnings` |
| `sectors` | "Sector performance" | `GET /api/v1/market/sectors` |
| `movers` | "Top movers today" | `GET /api/v1/market/movers` |
| `signals` | "AAPL signals" | `GET /api/v1/signals/generate` |
| `watchlist` | "My watchlist" | `GET /api/v1/watchlist/items` |
| `ai_portfolio` | "Analyze my portfolio" | `POST /api/v1/ai/advisor/portfolio` |
| `ai_market` | "Market analysis" | `POST /api/v1/ai/advisor/market` |
| `ai_risk` | "Risk assessment" | `POST /api/v1/ai/advisor/risk` |

The parser uses regex-based fallback (confidence ≥ 0.8) and falls back to AI-powered parsing for ambiguous queries.

---

### 🔷 Anomaly Detection

#### `GET /api/v1/analytics/anomaly/{ticker}`

Detect price anomalies for a ticker using z-score and IQR methods.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ticker` | string (path) | — | Ticker symbol |
| `method` | string | `zscore` | Detection method (`zscore` or `iqr`) |
| `threshold` | float | `3.0` | Z-score threshold |
| `period` | string | `6mo` | Lookback period |

**Response:** `200`
```json
{
  "ticker": "AAPL",
  "method": "zscore",
  "threshold": 3.0,
  "total": 126,
  "outlier_count": 2,
  "outlier_indices": [45, 98],
  "outlier_values": [195.50, 92.30]
}
```

**Backend implementation:** Uses Rust-based anomaly detection via PyO3 bindings (`miau_analytics`), including:
- **Z-score anomaly** — Flags points exceeding threshold standard deviations from mean
- **Isolation Forest** — Ensemble method for high-dimensional anomaly detection
- **Rolling window statistics** — Adaptive mean/std for time-series data

---

### 🔷 AGI (Artificial General Intelligence)

Autonomous financial AGI with self-improving strategies, causal inference, and safety guardrails.

| Endpoint | Description |
|---|---|
| `GET /api/v1/agi/status` | AGI system status, autonomy tier, safety checks |
| `GET /api/v1/agi/hypotheses` | Current market hypotheses being evaluated |
| `POST /api/v1/agi/tier` | Set autonomy tier (0-4) |

### 🔷 Quantum Computing

Quantum-classical hybrid algorithms for portfolio optimization, risk analysis, and options pricing.

| Endpoint | Description |
|---|---|
| `POST /api/v1/quantum/portfolio` | QAOA-based portfolio optimization (QUBO formulation) |
| `POST /api/v1/quantum/risk` | Quantum VaR using amplitude estimation |
| `POST /api/v1/quantum/options` | Quantum Monte Carlo options pricing |
| `POST /api/v1/quantum/hybrid` | Hybrid quantum-classical solver selector |

**Request (portfolio):**
```json
{
  "expected_returns": [0.12, 0.08, 0.15, 0.10],
  "covariance": [[0.04, 0.01], [0.01, 0.03]],
  "gamma": 1.0
}
```

**Response:** `200`
```json
{
  "weights": [0.35, 0.25, 0.30, 0.10],
  "expected_return": 0.115,
  "variance": 0.028,
  "sharpe_ratio": 2.15,
  "solver": "qaoa"
}
```

---

## Complete Endpoint Map (156+ Endpoints)

| # | Method | Path | Source |
|---|---|---|---|
| 1 | GET | `/api/v1/health` | main.py |
| 2 | GET | `/api/v1` | main.py |
| 3 | POST | `/api/v1/auth/token` | auth.py |
| 4 | GET | `/api/v1/ontology/types` | ontology.py |
| 5 | GET | `/api/v1/ontology/types/{type_id}` | ontology.py |
| 6 | GET | `/api/v1/ontology/types/{type_id}/properties` | ontology.py |
| 7 | GET | `/api/v1/ontology/links` | ontology.py |
| 8 | GET | `/api/v1/ontology/objects` | ontology.py |
| 9 | GET | `/api/v1/ontology/objects/{object_id}` | ontology.py |
| 10 | GET | `/api/v1/ontology/objects/{object_id}/links` | ontology.py |
| 11 | POST | `/api/v1/ontology/objects` | ontology.py |
| 12 | PUT | `/api/v1/ontology/objects/{object_id}` | ontology.py |
| 13 | POST | `/api/v1/ontology/links` | ontology.py |
| 14 | GET | `/api/v1/instruments` | instruments.py |
| 15 | GET | `/api/v1/instruments/{instrument_id}` | instruments.py |
| 16 | GET | `/api/v1/instruments/{instrument_id}/market-data` | instruments.py |
| 17 | GET | `/api/v1/instruments/sectors/list` | instruments.py |
| 18 | GET | `/api/v1/instruments/types/list` | instruments.py |
| 19 | GET | `/api/v1/portfolios` | portfolios.py |
| 20 | GET | `/api/v1/portfolios/{portfolio_id}` | portfolios.py |
| 21 | GET | `/api/v1/portfolios/{portfolio_id}/positions` | portfolios.py |
| 22 | GET | `/api/v1/portfolios/{portfolio_id}/trades` | portfolios.py |
| 23 | GET | `/api/v1/trades` | trades.py |
| 24 | GET | `/api/v1/trades/{trade_id}` | trades.py |
| 25 | GET | `/api/v1/search` | search.py |
| 26 | GET | `/api/v1/pipelines/runs` | pipelines.py |
| 27 | POST | `/api/v1/pipelines/runs` | pipelines.py |
| 28 | POST | `/api/v1/pipelines/calculate/pnl` | pipelines.py |
| 29 | GET | `/api/v1/analytics/summary` | combined.py |
| 30 | GET | `/api/v1/analytics/portfolios/{portfolio_id}` | combined.py |
| 31 | GET | `/api/v1/analytics/instruments/{instrument_id}/performance` | combined.py |
| 32 | GET | `/api/v1/analytics/pnl/timeseries` | combined.py |
| 33 | GET | `/api/v1/analytics/portfolios/{portfolio_id}/risk` | combined.py |
| 34 | GET | `/api/v1/market/live` | market.py |
| 35 | GET | `/api/v1/market/historical/{ticker}` | market.py |
| 36 | GET | `/api/v1/market/movers` | market.py |
| 37 | GET | `/api/v1/market/sectors` | market.py |
| 38 | GET | `/api/v1/market/indicators` | market.py |
| 39 | GET | `/api/v1/market/crypto` | market.py |
| 40 | GET | `/api/v1/market/crypto/top` | market.py |
| 41 | GET | `/api/v1/market/crypto/market` | market.py |
| 42 | GET | `/api/v1/market/crypto/fear-greed` | market.py |
| 43 | GET | `/api/v1/market/crypto/historical` | market.py |
| 44 | GET | `/api/v1/market/forex` | market.py |
| 45 | GET | `/api/v1/news/market` | news.py |
| 46 | GET | `/api/v1/news/company/{ticker}` | news.py |
| 47 | GET | `/api/v1/news/batch` | news.py |
| 48 | GET | `/api/v1/sentiment/sentiment` | sentiment.py |
| 49 | GET | `/api/v1/sentiment/sentiment/market` | sentiment.py |
| 50 | GET | `/api/v1/optimizer/optimize` | optimizer.py |
| 51 | GET | `/api/v1/optimizer/min-variance` | optimizer.py |
| 52 | GET | `/api/v1/optimizer/equal-weight` | optimizer.py |
| 53 | GET | `/api/v1/optimizer/performance` | optimizer.py |
| 54 | POST | `/api/v1/optimizer/black-litterman` | optimizer.py |
| 55 | GET | `/api/v1/risk/var` | risk.py |
| 56 | GET | `/api/v1/risk/beta` | risk.py |
| 57 | GET | `/api/v1/risk/stress-test` | risk.py |
| 58 | GET | `/api/v1/risk/greeks` | risk.py |
| 59 | GET | `/api/v1/risk/comprehensive` | risk.py |
| 60 | GET | `/api/v1/signals/generate` | signals.py |
| 61 | GET | `/api/v1/signals/multi` | signals.py |
| 62 | GET | `/api/v1/signals/backtest` | signals.py |
| 63 | GET | `/api/v1/fundamentals/{ticker}` | fundamentals.py |
| 64 | GET | `/api/v1/fundamentals/{ticker}/earnings` | fundamentals.py |
| 65 | GET | `/api/v1/fundamentals/{ticker}/filings` | fundamentals.py |
| 66 | GET | `/api/v1/fundamentals/{ticker}/insider-trades` | fundamentals.py |
| 67 | GET | `/api/v1/economics/*` | economics.py (5 endpoints) |
| 68 | GET | `/api/v1/economics/fred` | fred.py |
| 69 | GET | `/api/v1/options/{ticker}` | options.py |
| 70 | GET | `/api/v1/watchlist` | watchlist.py |
| 71 | POST | `/api/v1/watchlist` | watchlist.py |
| 72 | GET | `/api/v1/watchlist/items` | watchlist.py |
| 73 | POST | `/api/v1/watchlist/items` | watchlist.py |
| 74 | DELETE | `/api/v1/watchlist/items` | watchlist.py |
| 76 | GET | `/api/v1/analytics/monte-carlo` | monte_carlo.py |
| 77 | GET | `/api/v1/analytics/pairs/find` | pairs.py |
| 78 | GET | `/api/v1/analytics/pairs/backtest` | pairs.py |
| 79 | GET | `/api/v1/reports/*` | reports.py (3 endpoints) |
| 80 | WS | `/api/v1/ws/prices` | ws.py |
| 81 | POST | `/api/v1/orders` | orders.py |
| 82 | GET | `/api/v1/orders` | orders.py |
| 83 | GET | `/api/v1/orders/{id}` | orders.py |
| 84 | PUT | `/api/v1/orders/{id}` | orders.py |
| 85 | DELETE | `/api/v1/orders/{id}` | orders.py |
| 86 | GET | `/api/v1/orders/{id}/fills` | orders.py |
| 87 | POST | `/api/v1/paper-portfolios` | paper_portfolios.py |
| 88 | GET | `/api/v1/paper-portfolios` | paper_portfolios.py |
| 89 | GET | `/api/v1/paper-portfolios/{id}` | paper_portfolios.py |
| 90 | POST | `/api/v1/paper-orders` | paper_trades.py |
| 91 | GET | `/api/v1/paper-positions` | paper_trades.py |
| 92 | GET | `/api/v1/paper-trades` | paper_trades.py |
| 93 | GET | `/api/v1/paper-pnl` | paper_trades.py |
| 94 | GET | `/api/v1/brokers` | brokers.py |
| 95 | POST | `/api/v1/brokers/connect` | brokers.py |
| 96 | POST | `/api/v1/brokers/{name}/disconnect` | brokers.py |
| 97 | GET | `/api/v1/brokers/{name}/balance` | brokers.py |
| 98 | GET | `/api/v1/brokers/{name}/positions` | brokers.py |
| 99 | POST | `/api/v1/brokers/{name}/orders` | brokers.py |
| 100 | POST | `/api/v1/brokers/test` | brokers.py |
| 101 | POST | `/api/v1/brokers/{name}/sync` | brokers.py |
| 102 | GET | `/api/v1/currencies` | currencies.py |
| 103 | GET | `/api/v1/currencies/convert` | currencies.py |
| 104 | PUT | `/api/v1/portfolios/{id}/currency` | portfolios.py |
| 105 | GET | `/api/v1/markets/global` | markets.py |
| 106 | GET | `/api/v1/markets/global/{exchange}` | markets.py |
| 107 | GET | `/api/v1/analytics/portfolios/{portfolio_id}/fx-pnl` | combined.py |
| 108 | GET | `/api/v1/defi/wallet/chains` | wallet.py |
| 109 | POST | `/api/v1/defi/wallet/connect` | wallet.py |
| 110 | GET | `/api/v1/defi/wallet/sessions` | wallet.py |
| 111 | GET | `/api/v1/defi/wallet/sessions/{topic}` | wallet.py |
| 112 | POST | `/api/v1/defi/wallet/sessions/{topic}/disconnect` | wallet.py |
| 113 | POST | `/api/v1/defi/wallet/sessions/{topic}/chain` | wallet.py |
| 114 | POST | `/api/v1/defi/wallet/balances` | wallet.py |
| 115 | GET | `/api/v1/defi/protocols/uniswap/pool` | protocols.py |
| 116 | GET | `/api/v1/defi/protocols/uniswap/swap` | protocols.py |
| 117 | GET | `/api/v1/defi/protocols/aave/reserve` | protocols.py |
| 118 | GET | `/api/v1/defi/protocols/aave/deposit` | protocols.py |
| 119 | GET | `/api/v1/defi/protocols/aave/borrow` | protocols.py |
| 120 | GET | `/api/v1/defi/protocols/curve/pools` | protocols.py |
| 121 | GET | `/api/v1/defi/protocols/curve/pool/{pool_id}` | protocols.py |
| 122 | GET | `/api/v1/defi/protocols/lido/info` | protocols.py |
| 123 | GET | `/api/v1/defi/protocols/lido/stake` | protocols.py |
| 124 | GET | `/api/v1/defi/protocols/yearn/vaults` | protocols.py |
| 125 | GET | `/api/v1/defi/protocols/yearn/vault/{vault_id}` | protocols.py |
| 126 | GET | `/api/v1/defi/protocols/maker/vault-types` | protocols.py |
| 127 | GET | `/api/v1/defi/protocols/maker/simulate` | protocols.py |
| 128 | GET | `/api/v1/defi/protocols/solana/jupiter-pairs` | protocols.py |
| 129 | GET | `/api/v1/defi/protocols/solana/jupiter-swap` | protocols.py |
| 130 | GET | `/api/v1/defi/protocols/solana/raydium-pools` | protocols.py |
| 131 | GET | `/api/v1/defi/protocols/solana/raydium-lp` | protocols.py |
| 132 | GET | `/api/v1/defi/protocols/solana/marinade-info` | protocols.py |
| 133 | GET | `/api/v1/defi/protocols/solana/marinade-stake` | protocols.py |
| 134 | GET | `/api/v1/defi/protocols/yield/all` | protocols.py |
| 135 | GET | `/api/v1/defi/protocols/yield/best` | protocols.py |
| 136 | GET | `/api/v1/defi/protocols/yield/protocol` | protocols.py |
| 137 | GET | `/api/v1/defi/bridges/list` | bridges.py |
| 138 | GET | `/api/v1/defi/bridges/info` | bridges.py |
| 139 | GET | `/api/v1/defi/bridges/assets` | bridges.py |
| 140 | GET | `/api/v1/defi/bridges/simulate` | bridges.py |
| 141 | GET | `/api/v1/defi/nft/portfolio` | nft_tracker.py |
| 142 | GET | `/api/v1/defi/nft/floor/{collection}` | nft_floor.py |
| 143 | GET | `/api/v1/defi/nft/collections` | nft_floor.py |
| 144 | GET | `/api/v1/defi/nft/alert` | nft_floor.py |
| 145 | GET | `/api/v1/defi/nft/value` | nft_floor.py |
| 146 | GET | `/api/v1/defi/nft/listings` | nft_marketplace.py |
| 147 | GET | `/api/v1/defi/nft/listings/{listing_id}` | nft_marketplace.py |
| 148 | GET | `/api/v1/defi/nft/buy` | nft_marketplace.py |
| 149 | GET | `/api/v1/defi/nft/marketplaces` | nft_marketplace.py |
| 150 | POST | `/api/v1/quantum/portfolio` | quantum.py |
| 151 | POST | `/api/v1/quantum/risk` | quantum.py |
| 152 | POST | `/api/v1/quantum/options` | quantum.py |
| 153 | POST | `/api/v1/quantum/hybrid` | quantum.py |
| 154 | GET | `/api/v1/agi/status` | agi.py |
| 155 | GET | `/api/v1/agi/hypotheses` | agi.py |
| 156 | POST | `/api/v1/agi/tier` | agi.py |

---

---

## AI Advisor

All AI endpoints require JWT authentication and are rate-limited to 10 requests/minute per user.

### `POST /api/v1/ai/advisor/portfolio`

Analyze a portfolio using AI. Returns JSON with summary, strengths, weaknesses, recommendations, and risk level.

**Request body:**
```json
{
  "portfolio_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "data": {
    "summary": "Portfolio is well-diversified with moderate risk.",
    "strengths": ["Strong tech sector allocation", "Low correlation between holdings"],
    "weaknesses": ["Overweight in growth stocks", "No bond exposure"],
    "recommendations": ["Add 10% bond allocation", "Reduce AAPL position"],
    "risk_level": "medium"
  },
  "error": null
}
```

### `POST /api/v1/ai/advisor/market`

Analyze current market conditions. Returns sentiment, hot/cold sectors, opportunities, and risks.

**Response:**
```json
{
  "data": {
    "market_sentiment": "bullish",
    "hot_sectors": ["Technology", "Semiconductors"],
    "cold_sectors": ["Utilities", "Real Estate"],
    "opportunities": ["AI momentum plays", "Rate cut beneficiaries"],
    "risks": ["Valuation expansion", "Geopolitical tensions"]
  },
  "error": null
}
```

### `POST /api/v1/ai/advisor/risk`

Assess portfolio risk. Returns risk score, factors, and mitigation strategies.

**Request body:**
```json
{
  "portfolio_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "data": {
    "risk_score": "45",
    "risk_factors": ["High sector concentration", "Elevated volatility"],
    "mitigation": ["Diversify across sectors", "Add hedges"],
    "stress_test_results": {
      "market_crash": "-35% drawdown expected",
      "rate_hike": "-5% impact on duration-sensitive holdings"
    }
  },
  "error": null
}
```

### `POST /api/v1/ai/query`

Natural language query processing. Converts plain English queries into API calls and executes them.

**Request body:**
```json
{
  "query": "What is the current price of AAPL?"
}
```

**Response:**
```json
{
  "data": {
    "endpoint": "/api/v1/market/live",
    "params": {"tickers": "AAPL"},
    "data": {"AAPL": {"price": 150.25}},
    "explanation": "Fetching live price for Apple"
  },
  "error": null
}
```

**Supported query intents:** price, portfolio, holdings, risk, beta, news, fundamentals, watchlist, historical, options.

---

## Anomaly Detection

### `GET /api/v1/analytics/anomaly/{ticker}`

Detect price anomalies for a given ticker. Uses z-score and IQR methods.

**Parameters:**
- `ticker` (path) — Stock symbol (e.g., AAPL)
- `method` (query, optional) — `zscore` (default) or `iqr`
- `threshold` (query, optional) — Z-score threshold (default: 3.0)

**Response:**
```json
{
  "data": {
    "ticker": "AAPL",
    "method": "zscore",
    "threshold": 3.0,
    "total_points": 252,
    "outlier_count": 2,
    "outlier_values": [198.50, 95.20],
    "outlier_indices": [200, 245]
  },
  "error": null
}
```

---

---

## AI Advisor

### `POST /api/v1/ai/advisor/portfolio`

Analyze a portfolio using AI. Returns structured analysis with strengths, weaknesses, recommendations.

Request:
```json
{
  "portfolio_id": "uuid"
}
```

Response:
```json
{
  "summary": "Your portfolio is well-diversified...",
  "risk_level": "medium",
  "strengths": ["Strong sector diversification", "Low correlation between holdings"],
  "weaknesses": ["Overweight in tech sector"],
  "recommendations": ["Consider adding fixed income exposure"]
}
```

### `POST /api/v1/ai/advisor/market`

AI-powered market overview analysis.

Request:
```json
{}
```

Response:
```json
{
  "market_summary": "Markets are bullish...",
  "sectors": [{"name": "Technology", "outlook": "bullish"}]
}
```

### `POST /api/v1/ai/advisor/risk`

AI risk assessment for a portfolio.

Request:
```json
{
  "portfolio_id": "uuid"
}
```

Response:
```json
{
  "summary": "Portfolio risk is moderate...",
  "risk_level": "medium",
  "risk_factors": ["Concentration risk", "Sector correlation"],
  "mitigations": ["Hedge with inverse ETFs"]
}
```

### `POST /api/v1/ai/query`

General AI query — ask any finance question.

Request:
```json
{
  "query": "What is the P/E ratio of AAPL?"
}
```

Response:
```json
{
  "response": "Apple's trailing P/E ratio is approximately 28.5..."
}
```

---

## Natural Language Query (NLQ)

The NLQ endpoint converts plain English questions into structured API calls.

### `POST /api/v1/ai/query`

The NLQ parser extracts intent and parameters from natural language.

Supported intents: price lookup, portfolio listing, news search, fundamentals, signals, risk analysis.

Request:
```json
{
  "query": "what is the price of AAPL"
}
```

Response:
```json
{
  "intent": "price_query",
  "ticker": "AAPL",
  "response": "AAPL: $186.90 (+1.25%)"
}
```

---

## Anomaly Detection

### `GET /api/v1/analytics/anomaly/{ticker}`

Detect anomalous price movements for a given ticker using z-score and isolation forest algorithms.

Parameters:
- `ticker` (path) — Stock ticker symbol (e.g., AAPL)
- `threshold` (query, optional) — Z-score threshold (default: 3.0)
- `window` (query, optional) — Rolling window size (default: 20)

Response:
```json
{
  "ticker": "AAPL",
  "anomalies": [
    {"date": "2024-01-15", "price": 195.50, "z_score": 3.2},
    {"date": "2024-03-10", "price": 170.20, "z_score": -3.5}
  ],
  "total_anomalies": 2,
  "threshold": 3.0,
  "method": "z_score"
}
```

Status codes: `200` Success, `404` Ticker not found.

---

## Order Management

Orders allow creating, listing, viewing, modifying, and cancelling trades.

### `POST /api/v1/orders`

Create a new order.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `portfolio_id` | UUID | yes | Portfolio to place order in |
| `instrument_id` | UUID | yes | Instrument to trade |
| `order_type` | enum | yes | MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP |
| `side` | string | yes | BUY or SELL |
| `quantity` | number | yes | Number of units |
| `price` | number | no | Required for LIMIT/STOP_LIMIT |
| `stop_price` | number | no | Required for STOP/STOP_LIMIT/TRAILING_STOP |

Response: `201 Created` — The created order object.

### `GET /api/v1/orders`

List orders with optional filtering.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `portfolio_id` | UUID | — | Filter by portfolio |
| `instrument_id` | UUID | — | Filter by instrument |
| `status` | string | — | Filter by status (PENDING, SUBMITTED, FILLED, etc.) |
| `limit` | int | 50 | Max records |
| `offset` | int | 0 | Pagination offset |

### `GET /api/v1/orders/{order_id}`

Get a single order by ID.

### `PUT /api/v1/orders/{order_id}`

Modify an order (quantity, price, stop_price). Only PENDING or SUBMITTED can be modified.

### `DELETE /api/v1/orders/{order_id}`

Cancel an order. Only PENDING or SUBMITTED can be cancelled.

---

## Paper Trading

Paper trading provides a simulated environment for testing strategies without real capital.

### `POST /api/v1/paper/portfolios`

Create a paper trading portfolio.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | string | — | Portfolio name |
| `initial_cash` | number | 100000.0 | Starting cash balance |

### `GET /api/v1/paper/portfolios`

List all paper portfolios for the authenticated user.

### `GET /api/v1/paper/portfolios/{portfolio_id}`

Get paper portfolio details with buy/sell totals.

### `POST /api/v1/paper/execute/{portfolio_id}`

Execute a simulated trade.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `instrument_id` | UUID | yes | Instrument to trade |
| `side` | enum | yes | BUY or SELL |
| `quantity` | number | yes | Number of units |
| `order_type` | enum | yes | market, limit, stop, trailing_stop |
| `limit_price` | number | for limit | Limit price |
| `stop_price` | number | for stop | Stop price |
| `trail_pct` | number | for trailing_stop | Trail percentage |

### `GET /api/v1/paper/trades/{portfolio_id}`

Get trade history for a paper portfolio.

---

## Broker Integration

Connect to external brokers (Alpaca, Interactive Brokers) for real trading.

### `GET /api/v1/brokers`

List configured brokers.

### `GET /api/v1/brokers/{name}/account`

Get broker account information (cash, buying power, status).

### `POST /api/v1/brokers/{name}/orders`

Submit an order to a broker.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `ticker` | string | yes | Stock ticker |
| `side` | enum | yes | BUY or SELL |
| `quantity` | number | yes | Number of shares |
| `order_type` | enum | yes | market or limit |
| `limit_price` | number | for limit | Limit price |
| `time_in_force` | string | no | day, gtc, etc. |

### `DELETE /api/v1/brokers/{name}/orders/{order_id}`

Cancel an order on a broker.

---

## Order Management

Order management endpoints allow full order lifecycle management with multiple order types.

### `POST /api/v1/orders`

Create a new order with pre-trade risk checks.

**Request body:**
```json
{
  "portfolio_id": "uuid",
  "instrument_id": "uuid",
  "order_type": "market",
  "side": "BUY",
  "quantity": 100,
  "price": 150.00
}
```

**Order types:** `market`, `limit`, `stop`, `stop_limit`, `trailing_stop`

**Response:**
```json
{
  "id": "uuid",
  "portfolio_id": "uuid",
  "instrument_id": "uuid",
  "order_type": "market",
  "side": "BUY",
  "quantity": 100,
  "price": 150.00,
  "status": "PENDING",
  "created_at": "2025-01-15T12:00:00Z"
}
```

### `GET /api/v1/orders`

List orders with optional filters.

**Query parameters:**
- `portfolio_id` (optional) — Filter by portfolio
- `instrument_id` (optional) — Filter by instrument
- `status` (optional) — Filter by status (PENDING, SUBMITTED, FILLED, CANCELLED, REJECTED)
- `limit` (optional, default: 50) — Page size
- `offset` (optional, default: 0) — Pagination offset

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "ticker": "AAPL",
      "side": "BUY",
      "quantity": 100,
      "price": 150.00,
      "status": "FILLED",
      "created_at": "2025-01-15T12:00:00Z"
    }
  ],
  "total": 1
}
```

### `GET /api/v1/orders/{order_id}`

Get detailed order information including fills and status timeline.

**Response:**
```json
{
  "id": "uuid",
  "ticker": "AAPL",
  "side": "BUY",
  "order_type": "limit",
  "quantity": 100,
  "price": 150.00,
  "filled_quantity": 50,
  "status": "PARTIALLY_FILLED",
  "created_at": "2025-01-15T12:00:00Z",
  "fills": [
    {"quantity": 50, "price": 150.00, "filled_at": "2025-01-15T12:05:00Z"}
  ]
}
```

### `PUT /api/v1/orders/{order_id}`

Modify an open order (quantity, price, stop price).

**Request body:**
```json
{
  "quantity": 200,
  "price": 155.00
}
```

### `DELETE /api/v1/orders/{order_id}`

Cancel an open order (status must be PENDING or SUBMITTED).

**Response:** `200 OK` — Order cancelled

### `GET /api/v1/orders/{order_id}/fills`

Get fill history for a specific order.

---

## Paper Trading

Paper trading provides a simulated trading environment with realistic fill simulation, slippage, and transaction costs — no real money required.

### `POST /api/v1/paper-portfolios`

Create a new paper trading portfolio.

**Request body:**
```json
{
  "name": "My Paper Portfolio",
  "initial_cash": 100000
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "My Paper Portfolio",
  "cash": 100000,
  "market_value": 0,
  "total_value": 100000,
  "created_at": "2025-01-15T12:00:00Z"
}
```

### `GET /api/v1/paper-portfolios`

List all paper portfolios for the authenticated user.

### `GET /api/v1/paper-portfolios/{id}`

Get paper portfolio details including positions and P&L.

### `POST /api/v1/paper-orders`

Place a paper trade order.

**Request body:**
```json
{
  "ticker": "AAPL",
  "side": "BUY",
  "quantity": 100,
  "order_type": "market",
  "price": 150.00
}
```

Order types: `market`, `limit`, `stop`, `stop_limit`

### `GET /api/v1/paper-positions`

List current open paper trading positions.

### `GET /api/v1/paper-trades`

List paper trade history with fill details.

### `GET /api/v1/paper-pnl`

Get P&L summary with realized/unrealized breakdown, win rate, and best/worst trades.

**Response:**
```json
{
  "total_pnl": 1500.00,
  "unrealized_pnl": 500.00,
  "realized_pnl": 1000.00,
  "win_rate": 0.65,
  "total_trades": 40,
  "winning_trades": 26,
  "losing_trades": 14,
  "best_trade": {"ticker": "TSLA", "pnl": 350.00, "date": "2025-01-10"},
  "worst_trade": {"ticker": "AMD", "pnl": -200.00, "date": "2025-01-12"}
}
```

---

## Broker Integration

Connect to real broker APIs (Alpaca, Interactive Brokers) for live trading.

### `GET /api/v1/brokers`

List connected brokers with status and balance.

**Response:**
```json
{
  "brokers": [
    {"name": "alpaca", "status": "connected", "balance": 50000, "mode": "paper"}
  ]
}
```

### `POST /api/v1/brokers/connect`

Connect to a broker. Optionally test connection before activating.

**Request body:**
```json
{
  "name": "alpaca",
  "api_key": "your-api-key",
  "api_secret": "your-api-secret",
  "mode": "paper"
}
```

### `POST /api/v1/brokers/{name}/disconnect`

Disconnect a broker and remove credentials.

### `GET /api/v1/brokers/{name}/balance`

Get account balance for a specific broker.

### `GET /api/v1/brokers/{name}/positions`

Get current positions from a broker.

### `POST /api/v1/brokers/{name}/orders`

Submit a real order through a connected broker.

**Request body:**
```json
{
  "ticker": "AAPL",
  "side": "BUY",
  "quantity": 100,
  "order_type": "market"
}
```

### `POST /api/v1/brokers/test`

Test broker API connection without saving credentials.

### `POST /api/v1/brokers/{name}/sync`

Synchronize positions and balances from a broker.

---

## Notifications & Push

Web push notification support for alerts, trade execution, and daily summaries.

### `POST /api/v1/notifications/push/subscribe`

Subscribe to push notifications. Stores browser push subscription for the authenticated user.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `endpoint` | string | yes | Push service endpoint URL |
| `p256dh_key` | string | no | Client public key |
| `auth_key` | string | no | Client auth secret |

### `DELETE /api/v1/notifications/push/unsubscribe`

Remove a push subscription.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `endpoint` | string | yes | Subscription endpoint to remove |

---

## Social: Portfolio Sharing

Share portfolios publicly with a unique token link.

### `POST /api/v1/social/share`

Create a shareable portfolio link.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `portfolio_id` | UUID | yes | Portfolio to share |
| `is_public` | bool | no | Public access (default: true) |
| `expires_at` | datetime | no | Optional expiration |

Response:
```json
{
  "share_token": "abc123...",
  "share_url": "/api/v1/public/portfolio/abc123...",
  "is_public": true
}
```

### `GET /api/v1/social/leaderboard`

Get community leaderboard rankings.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `period` | string | all_time | Ranking period (all_time, monthly, weekly) |
| `metric` | string | total_return | Ranking metric |
| `limit` | int | 20 | Max results |

---

## Social: Activity Feed

Post activities and interact with the community.

### `POST /api/v1/social/activity`

Create a social activity entry (trade, milestone, etc.).

### `GET /api/v1/social/feed`

Get the activity feed. Supports cursor-based pagination.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `limit` | int | 20 | Items per page |
| `filter` | string | global | Feed filter: global, following, own |
| `cursor` | string | — | Pagination cursor |

### `POST /api/v1/social/feed/{activity_id}/comment`

Comment on an activity.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `activity_id` | UUID (path) | yes | Activity to comment on |
| `text` | string | yes | Comment content |
| `parent_id` | UUID | no | Reply to existing comment |

### `GET /api/v1/social/feed/{activity_id}/comments`

Get comments for an activity.

---

## Social: Follows & Reputation

Follow other traders and earn reputation badges.

### `POST /api/v1/social/follow/{user_id}`

Follow another user.

### `DELETE /api/v1/social/follow/{user_id}`

Unfollow a user.

### `GET /api/v1/social/reputation`

Get your reputation score and level.

### `GET /api/v1/social/badges`

List your earned badges and progress.

---

## Endpoint Index

| # | Method | Path | Source |
|---|--------|------|--------|
| 81 | POST | `/api/v1/ai/advisor/portfolio` | ai_advisor.py |
| 82 | POST | `/api/v1/ai/advisor/market` | ai_advisor.py |
| 83 | POST | `/api/v1/ai/advisor/risk` | ai_advisor.py |
| 84 | POST | `/api/v1/ai/query` | ai_advisor.py |
| 85 | GET | `/api/v1/analytics/anomaly/{ticker}` | anomaly.py |
| 86 | POST | `/api/v1/orders` | orders.py |
| 87 | GET | `/api/v1/orders` | orders.py |
| 88 | GET | `/api/v1/orders/{id}` | orders.py |
| 89 | PUT | `/api/v1/orders/{id}` | orders.py |
| 90 | DELETE | `/api/v1/orders/{id}` | orders.py |
| 91 | GET | `/api/v1/orders/{id}/fills` | orders.py |
| 92 | POST | `/api/v1/paper-portfolios` | paper_portfolios.py |
| 93 | GET | `/api/v1/paper-portfolios` | paper_portfolios.py |
| 94 | GET | `/api/v1/paper-portfolios/{id}` | paper_portfolios.py |
| 95 | POST | `/api/v1/paper-orders` | paper_trades.py |
| 96 | GET | `/api/v1/paper-positions` | paper_trades.py |
| 97 | GET | `/api/v1/paper-trades` | paper_trades.py |
| 98 | GET | `/api/v1/paper-pnl` | paper_trades.py |
| 99 | GET | `/api/v1/brokers` | brokers.py |
| 100 | POST | `/api/v1/brokers/connect` | brokers.py |
| 101 | POST | `/api/v1/brokers/{name}/disconnect` | brokers.py |
| 102 | GET | `/api/v1/brokers/{name}/balance` | brokers.py |
| 103 | GET | `/api/v1/brokers/{name}/positions` | brokers.py |
| 104 | POST | `/api/v1/brokers/{name}/orders` | brokers.py |
| 105 | POST | `/api/v1/brokers/test` | brokers.py |
| 106 | POST | `/api/v1/brokers/{name}/sync` | brokers.py |

---

---

## PWA Configuration

### Manifest

The PWA manifest at `/manifest.json` declares app metadata for installability:

```json
{
  "name": "Miau Finance",
  "short_name": "Miau",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a1a14",
  "theme_color": "#0a1a14",
  "icons": [
    {"src": "/icons/icon-192.svg", "sizes": "192x192", "type": "image/svg+xml"},
    {"src": "/icons/icon-512.svg", "sizes": "512x512", "type": "image/svg+xml", "purpose": "maskable"}
  ]
}
```

### Service Worker

The service worker at `/sw.js` handles:
- **Install**: Caches app shell (HTML, CSS, JS) for offline use
- **Activate**: Cleans old caches on version update
- **Fetch**: Serves from cache with network-first strategy for API calls
- **Background Sync**: Queues alerts and watchlist updates when offline
- **Push**: Receives and displays push notifications

Registration happens in `main.tsx` via `registerServiceWorker()`.

### Push Notifications API

Push notifications use the Web Push API with VAPID authentication.

#### `POST /api/v1/push/subscribe`

Subscribe to push notifications.

**Request body:**
```json
{
  "endpoint": "https://fcm.googleapis.com/...",
  "keys": {
    "p256dh": "base64-encoded-public-key",
    "auth": "base64-encoded-auth-secret"
  }
}
```

**Response:** `200 OK` — Subscribed successfully

#### `POST /api/v1/push/unsubscribe`

Unsubscribe from push notifications.

**Request body:**
```json
{
  "endpoint": "https://fcm.googleapis.com/..."
}
```

#### `GET /api/v1/notifications/history`

Get notification history with optional filters.

**Query parameters:**
- `user_id` (optional) — Filter by user
- `channel` (optional) — Filter by channel (`push`, `email`, `sms`, `in_app`)
- `type` (optional) — Filter by type (`price_alert`, `trade`, `ai_ready`, `daily_summary`)
- `days` (optional, default: 30) — Lookback window
- `limit` (optional, default: 100) — Page size
- `offset` (optional, default: 0) — Pagination offset

#### `GET /api/v1/notifications/stats`

Get notification delivery statistics for the last 7 days.

**Response:**
```json
{
  "period_days": 7,
  "total": 145,
  "by_channel": {"push": 100, "email": 30, "sms": 15},
  "by_type": {"price_alert": 80, "trade": 40, "daily_summary": 7, "ai_ready": 18}
}
```

---

## Billing & Subscriptions

### `POST /api/v1/billing/checkout`
Create a Stripe checkout session for subscription upgrade.

| Parameter | Type | Description |
|-----------|------|-------------|
| `tier` | string | `pro` or `enterprise` |

**Response:**
```json
{
  "url": "https://checkout.stripe.com/c/pay_cs_xxx",
  "tier": "pro",
  "session_id": "cs_xxx"
}
```

### `GET /api/v1/billing/subscription`
Get current user's subscription details.

**Response:**
```json
{
  "tier": "pro",
  "status": "active",
  "stripe_customer_id": "cus_xxx",
  "current_period_end": "2026-06-19T00:00:00",
  "created_at": "2026-05-19T00:00:00"
}
```

### `POST /api/v1/billing/webhook`
Stripe webhook endpoint (called by Stripe on subscription events).

| Header | Description |
|--------|-------------|
| `Stripe-Signature` | Signed webhook payload for verification |

**Events handled:** `checkout.session.completed`, `customer.subscription.deleted`, `customer.subscription.updated`

---

## API Key Management

### `POST /api/v1/api-keys`
Create a new API key with scoped permissions.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Human-readable key name |
| `scopes` | string[] | Permissions: `market:read`, `orders:create`, `portfolios:read`, `analytics:all` |

**Response:**
```json
{
  "id": "uuid",
  "name": "MyTradingBot",
  "key_prefix": "miau_a1b",
  "scopes": ["market:read", "orders:create"],
  "created_at": "2026-05-19T00:00:00"
}
```

### `GET /api/v1/api-keys`
List all API keys for the authenticated user.

### `DELETE /api/v1/api-keys/{key_id}`
Revoke an API key.

---

## Valuation (Investment Banking)

### `GET /api/v1/analytics/valuation/wacc/{ticker}`
Calculate Weighted Average Cost of Capital using CAPM.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | — | Stock symbol |

**Response:**
```json
{
  "ticker": "AAPL",
  "cost_of_equity": 0.0825,
  "cost_of_debt": 0.035,
  "beta": 1.2,
  "wacc": 0.081,
  "market_cap": 2900000000000,
  "enterprise_value": 2950000000000
}
```

### `GET /api/v1/analytics/valuation/dcf/{ticker}`
Run a Discounted Cash Flow model with 5-year projections.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | — | Stock symbol |
| `growth` | float | 0.05 | Annual FCF growth rate |
| `terminal_growth` | float | 0.025 | Perpetuity growth rate |
| `years` | int | 5 | Projection period (3-10) |
| `exit_multiple` | float? | null | Exit EBITDA multiple (disables Gordon Growth) |

**Response:**
```json
{
  "ticker": "AAPL",
  "wacc": 0.084,
  "fair_price": 178.20,
  "current_price": 186.90,
  "upside_pct": -4.7,
  "recommendation": "HOLD",
  "enterprise_value": 2427000000000,
  "projections": [
    {"year": 1, "fcf": 114695000000, "discount_factor": 1.08, "pv": 105783000000}
  ]
}
```

### `GET /api/v1/analytics/valuation/comps/{ticker}`
Run Comparable Company Analysis with sector peers.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | — | Stock symbol |

**Response:**
```json
{
  "ticker": "GOOGL",
  "sector": "Technology",
  "industry": "Internet Content",
  "pe_ratio": 25.4,
  "ev_ebitda": 17.2,
  "price_to_book": 7.30,
  "price_to_sales": 6.80,
  "eps": 5.92,
  "peers": ["AAPL", "MSFT", "META", "AMZN"]
}
```

### `GET /api/v1/analytics/valuation/lbo/{ticker}`
Run a Leveraged Buyout model.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | — | Stock symbol |
| `debt` | float | 0.60 | Debt percentage (30-90%) |
| `exit_year` | int | 5 | Holding period (3-10) |
| `exit_multiple` | float | 10.0 | EBITDA exit multiple |

**Response:**
```json
{
  "ticker": "AAPL",
  "moic": 1.5,
  "irr_pct": 8.4,
  "verdict": "OK LBO",
  "entry_ev": 2900000000000,
  "entry_debt": 1740000000000,
  "entry_equity": 1160000000000,
  "exit_equity": 1740000000000
}
```

---

## Scenario Analysis

### `GET /api/v1/analytics/scenario/{ticker}`
Run 6 predefined market scenarios against a ticker. Scenarios are beta-weighted.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | — | Stock symbol |

**Response:**
```json
{
  "ticker": "AAPL",
  "beta": 1.2,
  "current_price": 186.90,
  "drawdown_risk": -40.0,
  "scenarios": [
    {"label": "Bear Case (-20%)", "original_price": 186.90, "shocked_price": 149.52, "change_pct": -20.0},
    {"label": "Black Swan (-40%)", "original_price": 186.90, "shocked_price": 112.14, "change_pct": -40.0}
  ]
}
```

### `POST /api/v1/analytics/scenario/portfolio`
Run a portfolio-level scenario with custom tickers, weights, and market shock.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tickers` | string[] | — | Portfolio tickers |
| `weights` | string? | equal | Comma-separated weights |
| `market_shock` | float | -0.10 | Market shock (-50% to +50%) |

---

## Dividends

### `GET /api/v1/analytics/dividends/{ticker}`
Fetch dividend data for a ticker.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | — | Stock symbol |

**Response:**
```json
{
  "ticker": "AAPL",
  "dividend_yield": 0.48,
  "dividend_rate": 0.96,
  "payout_ratio": 15.3,
  "five_year_avg_yield": 0.82,
  "ex_dividend_date": "2026-06-01"
}
```

### `GET /api/v1/analytics/dividends/calendar`  
Get dividend calendar across multiple tickers with projected income.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tickers` | string | `AAPL,MSFT,JNJ,PG,KO,XOM` | Comma-separated tickers |

**Response:**
```json
{
  "total_annual_income": 8500.00,
  "total_quarterly_income": 2125.00,
  "monthly_income": 708.33,
  "holdings": [
    {"ticker": "AAPL", "dividend_yield_pct": 0.48, "annual_dividend": 0.96, "estimated_quarterly": 0.24}
  ]
}
```

---

## Risk: Rolling Metrics

### `GET /api/v1/analytics/risk/rolling`
Calculate rolling 12-month Sharpe ratio, volatility, and beta.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ticker` | string | `AAPL` | Stock symbol |
| `benchmark` | string | `SPY` | Benchmark index |
| `window` | string | `12mo` | Rolling window: `3mo`, `6mo`, `12mo`, `24mo` |
| `period` | string | `3y` | Historical data period |

**Response:**
```json
{
  "ticker": "AAPL",
  "benchmark": "SPY",
  "window": "12mo",
  "current_sharpe": 1.20,
  "current_volatility_pct": 25.3,
  "current_beta": 1.20,
  "rolling_sharpe": {
    "dates": ["2026-04-01", "2026-03-15"],
    "values": [1.4, 1.3]
  },
  "rolling_beta": {
    "dates": ["2026-04-01", "2026-03-15"],
    "values": [1.15, 1.18]
  }
}
```

---

## Webhook Management

### `POST /api/v1/webhooks`
Create a new webhook endpoint.

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | string | HTTPS endpoint URL |
| `events` | string[] | Event types: `trade.filled`, `alert.triggered`, `ai.analysis.complete`, `portfolio.shared` |

**Response:**
```json
{
  "id": "wh_uuid",
  "url": "https://my.app/events",
  "events": ["trade.filled"],
  "secret": "whsec_xxx",
  "created_at": "2026-05-19T00:00:00"
}
```

### `GET /api/v1/webhooks`
List all webhook endpoints.

### `DELETE /api/v1/webhooks/{webhook_id}`
Delete a webhook endpoint.

---

## Audit Log

### `GET /api/v1/audit/log`
Export audit log entries.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `days` | int | 7 | Number of days of history |
| `format` | string | `json` | Output format (`json` or `csv`) |
| `action` | string? | null | Filter by action type |

**Response (JSON):**
```json
{
  "count": 145,
  "days": 7,
  "entries": [
    {"timestamp": "2026-05-19T10:30:00", "user": "admin", "action": "order.create", "resource": "/api/v1/orders", "status": 200, "duration_ms": 45}
  ]
}
```

---

## Developer Console

### `GET /api/v1/api-keys`
List API keys (see API Key Management above).

### `GET /api/v1/usage`
Get usage statistics for the authenticated user's API keys.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `days` | int | 30 | Number of days of history |

**Response:**
```json
{
  "total_requests": 12500,
  "days": 30,
  "daily_average": 416,
  "by_key": [
    {"name": "MyTradingBot", "requests": 8500, "data_transfer_mb": 34.2}
  ]
}
```

> Full interactive documentation available at `http://localhost:8000/docs` (Swagger UI) when the backend is running.

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
  じしˍ,)ノ    "That's all the endpoints, human.
               Now go make some API calls. 🐱"
```

---

## Catberg — Bloomberg Terminal Emulation

Bloomberg Terminal function codes mapped to Catberg API, with real-time data and cat commentary.

### `GET /api/v1/catberg/{function_code}`

Returns pre-formatted data with cat commentary for any Bloomberg function code.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `function_code` | string | — | Bloomberg function code (WEI, N, WCV, GPO, etc.) |
| `ticker` | string? | null | Ticker for equity analysis functions |
| `category` | string? | null | Category filter for news (US, HOT) |
| `n` | int | 10 | Number of results (1-50) |

**Supported Function Codes:**

| Category | Functions |
|----------|-----------|
| **News** | N, TOP, READ, NI, TNI, CN, MCN |
| **Market Monitors** | WEI, WB, WCV, CBQ, IM, ECST, WECO, ACDR |
| **Equity Analysis** | DES, CN, GPO, GIP, ANR, EM, RV, FA, MGMT, PHDC |
| **Main Menus** | NRG, HYM, MA, FUND, EMKT, ET, IRSM |
| **Bonds** | YAS, WS |
| **Getting Started** | HELP, BACK, KB, PRINT |
| **Customization** | PDFQ, EASY, BLP |
| **Training** | TRAIN, DOCS |

**Example responses:** See [COMMANDS.md](COMMANDS.md) for terminal output examples.

---

## 📡 Datavore API (v2.3 Datavore Edition)

All endpoints under `/api/v1/datavore/` provide market data, fundamental analysis, and screening capabilities. Most require no API key (free tier).

### `GET /api/v1/datavore/screener`
Screen stocks by criteria.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `industry` | string | Filter by industry (Tech, Finance, Energy, etc.) |
| `minMcap` | number | Minimum market cap in billions |
| `maxMcap` | number | Maximum market cap in billions |
| `country` | string | Filter by country code (US, GB, JP, etc.) |
| `limit` | number | Max results (default 50) |

**Response:** `{ results: [{ ticker, name, industry, marketCap, price, change_pct }] }`

### `GET /api/v1/datavore/insider/{ticker}`
Insider trading transactions for a ticker.

**Response:** `{ ticker, transactions: [{ date, insider, type, shares, price }], net_buy_sell_ratio }`

### `GET /api/v1/datavore/short/{ticker}`
Short interest data.

**Response:** `{ ticker, short_interest, short_pct_float, days_to_cover }`

### `GET /api/v1/datavore/ipo`
IPO calendar.

**Response:** `{ ipos: [{ company, ticker, exchange, price_range, date, underwriters }] }`

### `GET /api/v1/datavore/ownership/{ticker}`
Institutional ownership data.

**Response:** `{ ticker, institutional_ownership_pct, top_holders: [{ name, shares, value }] }`

### `GET /api/v1/datavore/riskfactors/{ticker}`
AI-extracted risk factors from 10-K filings.

**Response:** `{ ticker, risk_factors: [{ category, word_count, trend }] }`

### `GET /api/v1/datavore/earningscore/{ticker}`
AI-scored earnings call transparency.

**Response:** `{ ticker, evasion_score (1-10), transparency_score, summary }`

### `GET /api/v1/datavore/profile/{ticker}`
Extended company profile.

**Response:** `{ ticker, name, industry, sector, employees, executives, peers, suppliers }`

### `GET /api/v1/datavore/fairvalue/{ticker}`
DCF fair value estimate.

**Response:** `{ ticker, fair_value, current_price, upside_pct, sensitivity_matrix }`

### `GET /api/v1/datavore/passiveflow/{ticker}`
ETF passive ownership analysis.

**Response:** `{ ticker, passive_ownership_pct, etfs_holding: [{ etf_name, shares }] }`

### `GET /api/v1/datavore/technicals/{ticker}`
Technical indicators (RSI, MACD, SMA, EMA, Bollinger, Stochastic).

**Response:** `{ ticker, rsi, macd: { value, signal, histogram }, sma: { 20, 50, 200 }, bollinger: { upper, middle, lower } }`

### `GET /api/v1/datavore/intraday/{ticker}`
Intraday OHLCV data.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `interval` | string | 1min, 5min, 15min (default 5min) |

**Response:** `{ ticker, bars: [{ timestamp, open, high, low, close, volume }] }`

### `GET /api/v1/datavore/famanch/{ticker}`
Fama-French 5-factor loadings.

**Response:** `{ ticker, factors: { mkt_rf, smb, hml, rmw, cma }, r_squared }`

### `GET /api/v1/datavore/dividend/{ticker}`
Dividend history and metrics.

**Response:** `{ ticker, dividend_history: [{ date, amount }], growth_streak_years, payout_ratio }`

### `GET /api/v1/datavore/catalyst/{ticker}`
SEC filing catalysts.

**Response:** `{ ticker, filings: [{ type (8-K/10-Q/10-K), date, description, link }] }`

## 📊 Market Data Providers

The Datavore layer aggregates data from 25+ providers:

**No-Key Providers (free):**
- Yahoo Finance — quotes, news, fundamentals
- StockPrice.dev — real-time prices
- Frankfurter — FX rates (200 currencies, 1948+)
- DeFiLlama — TVL, yields, DEX volumes, stablecoins
- SecuritiesDB — Piotroski F-Score, Altman Z, DCF, ETF overlap
- DumbStock — ticker symbols/metadata
- Blocknative — gas prices for 40+ chains
- CEX (Binance/Coinbase/Kraken) — ticker, order book, trades

**Key-Based Providers (API key required):**
- Finnhub — quote, candles, profile, financials, news, SEC, earnings
- Twelve Data — real-time/historical, 100k+ instruments, WebSocket
- CoinPaprika — 2000+ coins, market data
- BLS — CPI, PPI, employment
- Etherscan — gas tracker

## 📋 Log & Monitoring API

### `GET /api/v1/health`
System health endpoint.

**Response:** `{ status, version, uptime_seconds, services: {...}, provider_health: {...}, data_providers: number }`

### `GET /api/v1/logs/files`
List available log files (requires auth).

**Response:** `{ files: [{ path, size_bytes, modified }] }`

## 🎯 Marketing API

### `POST /api/v1/marketing/track`
Track marketing conversion event (public).

**Body:** `{ event, source, campaign, referrer }`

### `GET /api/v1/marketing/conversions`
Get conversion metrics (requires auth).

## 🔐 Auth API

### `POST /api/v1/auth/education-student`
Create education portal token. **Requires `Authorization: Bearer <education_api_key>` header.**

**Response:** `{ access_token, token_type }`

---

## V6 — MiauGlobe Data Layers

### `GET /api/v1/datavore/globe/layer/{layer_id}`

Fetch data for a single globe layer. Returns formatted geoJSON-like array for rendering on MiauGlobe.

| Layer ID | Provider | Data |
|----------|----------|------|
| `aircraft` | OpenSky | Live ADS-B flights with callsign, origin, altitude, speed, heading |
| `maritime` | Maritime | 40 ports, ship positions, 30 shipping lanes |
| `military_bases` | Geopolitical | 60 bases: name, country, branch, personnel |
| `nuclear` | Geopolitical | 36 nuclear facilities: name, country, type, capacity |
| `defense_spending` | Geopolitical | 10-country defense budget ($, %GDP) |
| `mining` | Mining | 50 mines: name, commodity, owner, production, country |
| `oil_fields` | Energy | 41 oil/gas fields: name, country, type, daily_bbl |
| `renewable` | Energy | 32 renewable: hydro/wind/solar with capacity_mw |
| `companies` | Corporate | 42 Fortune HQ: name, ticker, industry, revenue_b, lat/lng |
| `cargo` | Cargo | 10 FedEx/UPS/DHL hubs, 18 freight routes |
| `satellites` | Celestrak | 17 orbital objects with live Keplerian position |
| `ufo` | Alien | 25 UFO sighting locations |
| `ancient_sites` | Alien | 20 ancient astronaut theory sites |
| `conflicts` | Conflict | 25 active conflict zones |
| `supply_chain` | Corporate + Cargo | Combined company HQ + cargo hub data |

### `GET /api/v1/datavore/globe/batch?layers=aircraft,maritime,satellites`

Fetch multiple layers in one request. Comma-separated layer IDs. Returns `{ "layers": { ... }, "count": N }`.

### `GET /api/v1/datavore/globe/layers`

List all available globe layers with their metadata (name, description, data counts).

---

---

## 🐱 Miau DatChonk — Data Eating Service

Miau DatChonk is a background service that continuously pre-fetches and caches market data. The main backend checks Chonk first before making live API calls, making price lookups **instant**.

### Chonk API (`http://localhost:8765`)

| Endpoint | Description |
|----------|-------------|
| `GET /` | Web page with DatChonk UI (food rain, chonky cat, live data) |
| `GET /health` | JSON status — cached entries count |
| `GET /price/{ticker}` | Get cached price for one ticker |
| `GET /prices?tickers=AAPL,TSLA,MSFT` | Get cached prices for multiple tickers |
| `GET /chonk` | Full cache status with all entries |

### How to Use

```bash
# Terminal (instant from cache)
price AAPL

# Terminal (force live data)
price AAPL -l

# Direct API (instant from Chonk)
curl http://localhost:8765/prices?tickers=AAPL,TSLA

# Direct API (with live flag)
curl "http://localhost:8000/api/v1/market/live?tickers=AAPL&live=true"
```

The `?live=true` query parameter bypasses the Chonk cache and fetches fresh data from Yahoo Finance.

---

## 🖥️ Kittyland — Floating Panel System

Kittyland is a draggable, pinnable floating panel system that lets you view command output in persistent panels alongside your terminal. Like Hyprland, but inside your terminal.

### Commands

| Command | Description |
|---------|-------------|
| `price AAPL -p` | Opens any command output in a floating panel |
| `kitty` | Show Kittyland help |
| `kitty ls` | List open panels |
| `kitty close 1` | Close panel #1 |
| `kitty clear` | Close all panels |

Append `-p` or `--panel` to **any** command to open its output in a floating panel.

---

## V6 — MiauGlobe Terminal Commands (57+ commands)

| Command | Action |
|---------|--------|
| `miaumap` | Toggle 3D WebGL globe (GPU-accelerated globe.gl) |
| `miaumap --cats` | Open globe with cat layer activated |
| `miaumap --aliens` | Open globe with alien layer unlocked |
| `miauglobe` / `globe` | Aliases for miaumap |
| `map2d` | Toggle 2D canvas orthographic globe |
| `map` | Toggle Leaflet flat map |
| `fx [base]` | Live FX rates for 200+ currency pairs |
| `gas` | Ethereum gas prices |

---
