PROMPT_TEMPLATE = """Convert this natural language query to an API call.

Query: {query}

Available endpoints:
- GET /api/v1/market/live?tickers=... — Live prices for tickers
- GET /api/v1/market/historical/{ticker}?period=... — Historical prices
- GET /api/v1/market/movers — Market movers
- GET /api/v1/market/sectors — Sector performance
- GET /api/v1/market/indicators — US economic indicators
- GET /api/v1/news/market — Market news
- GET /api/v1/news/company/{ticker} — News for a company
- GET /api/v1/portfolios — List portfolios
- GET /api/v1/portfolios/{id} — Portfolio detail
- GET /api/v1/portfolios/{id}/positions — Portfolio positions
- GET /api/v1/analytics/summary — Analytics summary
- GET /api/v1/analytics/portfolios/{id} — Portfolio analytics
- GET /api/v1/fundamentals/{ticker} — Fundamentals for a ticker
- GET /api/v1/fundamentals/{ticker}/earnings — Earnings for a ticker
- GET /api/v1/watchlist/items — Watchlist items
- POST /api/v1/watchlist/items — Add to watchlist
- GET /api/v1/options/{ticker} — Options chain
- GET /api/v1/economics/fred?series_ids=... — FRED economic data
- GET /api/v1/risk/var?ticker=...&confidence=... — Value at Risk
- GET /api/v1/signals/generate?ticker=... — Trading signals
- GET /api/v1/analytics/sentiment?ticker=... — Sentiment analysis
- POST /api/v1/ai/advisor/portfolio — AI portfolio analysis
- POST /api/v1/ai/advisor/market — AI market analysis
- POST /api/v1/ai/advisor/risk — AI risk assessment
- POST /api/v1/ai/query — Ask AI anything

Respond with JSON only:
{
  "endpoint": "the API path",
  "method": "GET or POST",
  "params": {"key": "value"},
  "explanation": "brief explanation"
}"""
