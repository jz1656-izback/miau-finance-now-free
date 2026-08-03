# 🐱 V3 — Datavore Edition (50+ Providers, 515+ Endpoints)

> **Shipped as v2.3.0** — the "vacuum cleaner" release
> **Tests:** 136 new · **Commands:** 50+ new · **Endpoints:** 515+

---

## F-000: Foundation — Unified Data Source Layer

| Task | What |
|------|------|
| DataSource base class | Abstract provider with health, fallback, caching |
| Provider registry | Auto-discovery of registered providers |
| Redis cache layer | TTL-based caching with hit/miss tracking |
| Circuit breaker | Auto-skip failing providers after threshold |
| API key settings UI | Frontend settings page for third-party keys |
| 34 data source tests | Base, registry, cache, fallback, rate limit |

## P1-000: Market Data APIs (7 providers, 18 commands)

| Provider | Type | Key Required | Endpoints |
|----------|------|-------------|-----------|
| **Finnhub** | Stocks/crypto | ✅ | Quote, candles, profile, financials, news, SEC, earnings, IPO, insider, ownership, short interest, technicals |
| **SecuritiesDB** | Quant analytics | ❌ No key | Piotroski F-Score, Altman Z, DCF, ETF overlap, passive float, risk factors, Fama-French |
| **StockPrice.dev** | Real-time prices | ❌ No auth | Stock prices, no limits |
| **DumbStockAPI** | Ticker metadata | ❌ No key | Global ticker symbols, exchange metadata |
| **Twelve Data** | 100k+ instruments | ✅ | Real-time/historical, WebSocket, 50+ technical indicators |
| **Alpha Vantage** | 48 technical indicators | ✅ | RSI, MACD, BBANDS, SMA, EMA, STOCH, ADX, ATR, OBV, WILLR + 37 more |
| **HF Data Library** | 1-min OHLCV | ✅ | 1,391 US equities, 23+ years of minute data |

**Commands:** screener, etfanalyzer, insider, short, ipo, dividend, ownership, quanthealth, fairvalue, passiveflow, catalyst, riskfactors, earningscore, famanch, ticker, intraday, technicals, profile

## P2-000: DeFi & Crypto APIs (6 providers, 10 commands)

| Provider | Data | Key Required |
|----------|------|-------------|
| **DeFiLlama** | TVL, yields, DEX volumes, stablecoins, fees, bridges (2,400+ protocols) | ❌ No key |
| **CoinPaprika** | 2,000+ coins, market data, ICOs, exchanges | ✅ |
| **Blocknative** | Gas prices for 40+ chains | ❌ No key |
| **Etherscan** | Ethereum gas tracker, SafeGasPrice | ✅ |
| **CEX (Binance/Coinbase/Kraken)** | Ticker, order book, trades | ❌ No key |
| **Mobula** | On-chain wallet portfolio, token prices | ✅ |

**Commands:** defillama, yields, stablecoins, gas, dexs, fees, crosschain, tvl, stablecoin, chain

## P3-000: FX & Macro APIs (5 providers, 12 commands)

| Provider | Data | Key Required |
|----------|------|-------------|
| **Frankfurter** | 200 currencies, 55 central banks, history back to 1948 | ❌ No key |
| **BLS** | CPI, PPI, employment, unemployment, wages | ✅ |
| **EIA** | Oil, gas, coal, electricity, renewable energy | ✅ |
| **IMF** | GDP, inflation, trade, debt by country | ✅ |
| **FRED** | 800,000+ US economic time series | ✅ |

**Commands:** fx, fxhistory, fxconvert, cpi, inflation, employment, energy, agriculture, gdp, macro, treasury, indicators

## P4-000: Calculator Suite (15 commands)

| Command | Description |
|---------|-------------|
| `dca` | DCA backtest with final value, CAGR |
| `compound` | Compound interest with schedule |
| `retirement` | Retirement projection with chart |
| `loan` | Loan amortization, total interest |
| `margin` | Margin liquidation price calculator |
| `rebalance` | Tax-aware portfolio rebalancing |
| `benchmark` | Tracking error, alpha, beta, info ratio |
| `drawdown` | Max drawdown, recovery period |
| `montecarlo` | Monte Carlo price paths |
| `blacklitterman` | Prior + views → posterior weights |
| `riskparity` | Equal risk contribution weights |
| `pairtrade` | Cointegration, spread, z-score |
| `optionspayoff` | P&L diagram (covered call, straddle) |
| `taxlot` | FIFO/LIFO gain/loss |
| `correlation` | Full correlation matrix heatmap |

## P5-000: AI Intelligence Commands (8 commands)

| Command | Description |
|---------|-------------|
| `aisummary` | 3-paragraph company summary from filings + news |
| `aisentiment` | Multi-source sentiment (news, social, filings, earnings) |
| `aiinsight` | Deep research: moat, risks, catalysts, valuation |
| `aireport` | Daily/weekly AI market report |
| `aiallocate` | Portfolio allocation by risk profile |
| `airisk` | Narrative risk assessment |
| `aitrade` | AI analyzes, generates thesis, executes paper trade |
| `aichooser` | AI picks best investment with reasoning |

## P6-000: Map & Shell Polish

| Task | What |
|------|------|
| Leaflet zoom fix | `minZoom`, `maxBounds`, `maxBoundsViscosity` |
| Boat/jet markers | Clickable with route popups |
| Company panel | 960px detail panel with tabs |
| Weather overlay | RainViewer radar precipitation layer |
| Search | Match highlighting, keyboard nav, result count |
| Panel transitions | CSS animations: fade-in, zoom-in |
| IB valuation fix | Edge cases: wacc==terminal_growth, zero division |

## P7-000: Education Platform

| Course | Content |
|--------|---------|
| Data Sources | How the vacuum cleaner works |
| Stock Screening | screener, quanthealth, fairvalue |
| DeFi Analytics | yields, tvl, stablecoins, gas |
| Macro & FX | fx, cpi, inflation, gdp |
| Financial Calculators | dca, compound, retirement, loan |
| AI Research | chartz, quanthealth, fairvalue, montecarlo |
| Shell Maniac | 50+ new commands, Datavore lesson |

## V3 Infrastructure

| Feature | Details |
|---------|---------|
| Catberg | 30+ Bloomberg-style live-data panels (WEI, N, WCV, WB, IM, ECST, CBQ, DES, GPO, GIP, ANR, EM, RV, FA, CN, MGMT, PHDC) |
| WorldMap | Continent-sharded companies (7 shards, lazy-loaded), RainViewer weather overlay, 50x faster batch markers |
| MiauGlobe | GPU-accelerated 3D globe (Globe.gl), company points, trade route arcs, auto-rotation |
| Log Viewer | `/logs-viewer/` — real-time log tailing, filters, stats, themes |
| Health check | 6.7s → 0.47s via parallel `asyncio.gather` |
| 15 command API fixes | All return HTTP 200 with fallback data |
| Scheduler fix | 81× billing_balances errors resolved |
| chartz enhancement | `-l` live/news, `-m` mega/BBands/SR, `-lm` max/cats, `-c` CSV export |
| Yahoo News API | Free news with clickable links |
| Fama-French 5-factor | `famanch` command |
| Auth security audit | 5 vulnerabilities fixed |
| 5 MiauPapers | #71–75: Wirecard, Trade Republic, German SaaS, BaFin, Würselen to Wall Street |
