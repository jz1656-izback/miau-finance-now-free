# Miau Finance v2.3.0 — Datavore Edition 🐱💨

**Released:** May 2026  
**Repository:** [github.com/LuZziD/cat-finance-analytics-shell-miau](https://github.com/LuZziD/cat-finance-analytics-shell-miau)

> *"i wanna pull data like a vacuum cleaner from public apis" — the cat*

---

## What's New in v2.3.0

### 📡 25+ API Providers — 8 No-Key, 5 Key-Based

The biggest data expansion in Miau history. The Datavore Edition adds **25+ API providers** sucking data from every corner of finance:

| Category | No-Key Providers | Key-Based Providers |
|----------|-----------------|-------------------|
| **Market Data** | Yahoo Finance, StockPrice.dev, DumbStockAPI, SecuritiesDB | Finnhub, Twelve Data |
| **DeFi/Crypto** | DeFiLlama, Blocknative, CEX (Binance/Coinbase/Kraken) | CoinPaprika, Etherscan |
| **FX/Macro** | Frankfurter API (200 currencies, 1948+) | BLS (CPI/employment) |
| **Economic** | IMF Data Explorer, World Bank, FRED | — |
| **Energy** | EIA (oil/gas/coal/electricity) | — |
| **Other** | Mobula (on-chain wallets) | — |

### ⌨️ 50+ New Terminal Commands

| Category | Commands |
|----------|---------|
| **Screening** | `screener` — screen by industry/mcap/country |
| **Fundamental** | `insider`, `short`, `ipo`, `ownership`, `profile`, `quanthealth`, `fairvalue`, `passiveflow`, `riskfactors`, `earningscore` |
| **Data** | `ticker`, `intraday`, `technicals`, `famanch`, `dividend`, `catalyst` |
| **DeFi** | `defillama`, `yields`, `stablecoins`, `gas`, `dexs`, `fees`, `crosschain`, `tvl`, `stablecoin`, `chain` |
| **Macro** | `fx`, `fxhistory`, `fxconvert`, `cpi`, `inflation`, `employment`, `energy`, `agriculture`, `gdp`, `macro`, `treasury`, `indicators` |
| **Calculators** | `dca`, `compound`, `retirement`, `loan`, `margin`, `rebalance`, `benchmark`, `drawdown`, `montecarlo`, `blacklitterman`, `riskparity`, `pairtrade`, `optionspayoff`, `taxlot`, `correlation` |
| **AI** | `aisummary`, `aisentiment`, `aiinsight`, `aireport`, `aiallocate`, `airisk`, `aitrade`, `aichooser` |

### 🎓 120 Courses & 18 Certifications

From 21 courses (v2.1) to **120 courses** and **18 certifications**. New courses include:
- Miau Finance Data Sources
- Advanced Stock Screening & Quant Analysis
- DeFi Analytics with DeFiLlama
- Macro & FX Analysis
- Financial Calculators & Planning
- AI-Powered Investment Research
- 46 additional courses covering everything from AGI ethics to agricultural finance

### 📊 chartz Overhaul

| Flag | Mode | Description |
|------|------|-------------|
| `-l` | Live + News | Real-time price with Yahoo Finance news feed |
| `-m` | Mega | 22 rows + 90 cols, Bollinger Bands + Support/Resistance |
| `-lm` | Max + Cats | Full terminal + floating cat emojis on price action |
| `-c` | CSV Export | Export chart data to CSV for external analysis |

### 🔐 Security Audit — 5 Vulnerabilities Fixed

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 1 | `create_education_token` issued free JWTs | 🔴 CRITICAL | Now requires `education_api_key` Bearer token |
| 2 | `validate_user` timing attack (string `==`) | 🟡 HIGH | Replaced with `hmac.compare_digest()` |
| 3 | `refresh_access_token` refreshed without re-auth | 🟡 HIGH | Now requires username + password |
| 4 | CSRF bypass too broad (`/api/v1/education/*`) | 🟡 HIGH | Tightened to specific paths only |
| 5 | Missing `EDUCATION_API_KEY` in `.env.example` | 🟢 MED | Added to template |

All 50+ API routers verified with `dependencies=auth_deps` at router level. Security headers comprehensive (CSP, HSTS, XFO, COEP/COOP). CSRF token rotated per session.

### 🐱 Fama-French 5-Factor

New `famanch` command computes Fama-French 5-factor loadings (Market, Size, Value, Profitability, Investment) for any ticker — directly from the terminal, no API key needed.

### Other Improvements

- Boat/jet animation smoothness during map zoom
- Yahoo Finance news API — free, no key needed, real headlines with clickable links
- Education API key auth added to config
- Flag parsing made case-insensitive across all commands
- Auth security hardened across all middleware

---

## Upgrading from v2.1.0

```bash
git pull origin dev
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

# Miau Finance v2.1.0 — Pawborghini Edition

**Released:** May 2026  
**Repository:** [github.com/LuZziD/cat-finance-analytics-shell-miau](https://github.com/LuZziD/cat-finance-analytics-shell-miau)

---

## What's New in v2.1.0

### 🌍 WorldMap v3 — Leaflet with Google Maps-Style UX

| Feature | Description |
|---------|-------------|
| **OpenStreetMap tiles** | Three layers: street, satellite (ESRI), and dark (CartoDB) — toggle with one button |
| **Search & fly-to** | Search 100+ companies, press Enter or click result to fly to location + open detail panel |
| **50 markets, 100+ companies** | CircleMarkers visible at all zoom levels with ticker, price, change badges |
| **5-tab detail panel** | 📊 Info, 📈 Chart (1M/3M/6M/1Y/5Y), 📋 Stats (P/E, margins, ROE), 🏢 Peers, 📰 News |
| **🏦 Investment Banking** | DCF, WACC, Comps, LBO valuation endpoints with BUY/HOLD/SELL ratings |
| **🐱 Cat-jets** | All capital flows show 🐱✈️ emojis — cats on every boat and plane |
| **Panel 720px wide** | Custom `w-panel` Tailwind class, larger fonts, better readability |

### 📰 News API Rewrite

- Yahoo Finance search API primary source → yfinance fallback → hardcoded fallback
- Realistic headlines for AAPL/MSFT/GOOGL/AMZN/NVDA/TSLA

### 🛠️ Build & Infrastructure

- Build unblocked: 7 unused declarations removed, lint errors fixed
- Tailwind config: custom `w-panel`/`max-w-panel`/`max-h-panel` theme values
- Education platform service added to docker-compose.yml (port 5174)

### 🎓 Education Platform

- Standalone React+Vite app at `localhost:5174`
- 20 courses, pricing tiers, auth, interactive terminal simulator
- LIVE API proxy — real market data when logged in

### 📚 Documentation & Marketing

- Docs consolidation: 25+ MD files → 4 core + docs/ directory
- Screenshots (6), OG image (1200×630), sitemap (13 URLs)
- Catberg Bloomberg emulation with 41 function codes

### 🔐 Security

- JWT auth with bcrypt, RBAC, rate limiting, CSRF, CORS, CSP, audit logging
- All marketing files license fixed to Proprietary

---

## Upgrading from v1.0.0

```bash
git pull origin main
docker compose down
docker compose build --no-cache
docker compose up -d
docker compose exec backend alembic upgrade head
```

---

# Miau Finance v1.0.0 — Autonomous Finance GA

**Released:** May 2026  
**Repository:** [github.com/LuZziD/cat-finance-analytics-shell-miau](https://github.com/LuZziD/cat-finance-analytics-shell-miau)

---

## What's New in v1.0.0

After 17 phases of development, Miau Finance ships its General Availability release. This is the culmination of 400+ commits, 44 microtasks in the final phase alone, and countless cat naps.

### 🏆 GA Features

| Feature | Description |
|---------|-------------|
| **Auto-Rebalance** | Detect portfolio drift, generate rebalance plans, set target allocations — all from the terminal |
| **Portfolio Export** | Export portfolios to JSON, CSV, or PDF with one command |
| **Miau Score** | Composite score combining Sharpe ratio, ESG rating, and portfolio diversity |
| **Cat Companion** | Animated cat that reacts to your portfolio P&L — purrs on gains, hides on losses |
| **Achievement System** | Unlock achievements for milestones: first trade, 100% returns, diamond hands, and more |
| **Ctrl+R History** | Fuzzy-search through your command history (tmux/readline style) |
| **v1.0.0 Welcome Screen** | Animated boot sequence showing the Miau Finance logo, version, and cat art |
| **MiauPapers Reader** | Read whitepapers directly in the terminal with `miaupapers` command |
| **Tuna Counter** | Track your earned tuna in the terminal status bar |

### 🎯 Release Stabilization

- Full test suite passing (280+ tests)
- Edge case hardening across all services
- Security audit (bandit, SAST, dependency scan)
- Rate limit tuning for production workloads
- CORS & CSP headers hardened
- Structured logging with JSON output
- Docker production config with health checks
- Kubernetes GA manifests
- Load tested to 1000 concurrent connections

### 📚 Documentation

- [Self-hosted deployment guide](docs/DEPLOY.md)
- [API reference](docs/API.md) (100+ endpoints)
- [Terminal commands](docs/COMMANDS.md) (60+ commands)
- [Architecture overview](docs/ARCHITECTURE.md)
- [Security architecture](docs/SECURITY.md)

---

## What Came Before (Phase Highlights)

| Phase | Theme | Highlights |
|-------|-------|-----------|
| **1-10** | Foundation | Terminal UI, market data, portfolios, analytics, AI advisor, social, mobile |
| **11** | Monetization | Stripe subscriptions, API keys, tier middleware, usage billing |
| **12** | Enterprise | SSO, audit log, admin dashboard, SOC2 compliance checklist |
| **12.5** | Visual Polish | 3D Globe map, correlation heatmap, benchmark comparison, sector peers |
| **13** | AI-Native Terminal | Voice commands, AI autocomplete, multi-step agentic workflows |
| **14** | Global Markets | Multi-currency (20 currencies), 40 intl exchanges, 5 broker connectors, i18n (8 languages) |
| **15** | Developer Platform | Python SDK, plugin system, curl API examples |
| **16** | ESG & Sustainability | ESG scores, carbon footprint tracking, portfolio carbon intensity |
| **17** | **v1.0.0 GA** | Auto-rebalance, portfolio export, Miau Score, cat companion, release stabilization |

---

## Quick Start

```bash
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd miau-finance
cp .env.example .env
make up
```

Then open **http://localhost:5173** and type `help` to see all commands.

---

## Upgrading from v0.x

If you have an existing deployment:

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker compose down
docker compose build --no-cache
docker compose up -d

# Run any new migrations
docker compose exec backend alembic upgrade head
```

See the [upgrade guide](docs/DEPLOY.md#upgrading) for detailed instructions.

---

## Changelog

Full commit history: [CHANGELOG.md](CHANGELOG.md)

## License

MIT — see [LICENSE](LICENSE)

---

```
  ╱|、
 (˚ˎ 。7     "v1.0.0. The cat is out of the bag."
  |、˜〵      "Go make some fish, human. 🐟"
  じしˍ,)ノ
```

---

# 🐱💸 Miau Finance v9.0.0 — "The Cat Gets Paid" Edition 🐱💸

**Released:** May 2026

> *"The cat built a Bloomberg. The cat hired interns. The cat is now accepting payments."*

---

## What's New in v9.0.0

### 💳 Monetization — The Cat Gets Paid

- **Stripe checkout integration** — `billing upgrade` opens Stripe for €99/mo Pro
- **Revenue tracking** — `revenue` shows 20/80 split, revenue history, projections
- **Pricing page** — `pricing` command + ecosystem site with €99 Pro / €396 Enterprise
- **PayPal invoicing** — `invoice pro` generates PayPal.me link for any tier
- **i-paid** — activates tier after manual payment with verification
- **Tuna top-up** — `topup` command, buy tuna packs (€1.99–€99.99)
- **CFO Dashboard** — `cfodashboard` shows revenue, ops budget, penthouse fund progress
- **Donate command** — crypto + fiat donation addresses

### 🤖 AI & Quant — Cat Learns to Trade

- **Technical Analysis engine** — 17 indicators (SMA, EMA, MACD, RSI, BB, ATR, ADX, Stoch, OBV, Ichimoku, Aroon, Williams %R, MFI, CCI, Demark, ROC, Keltner)
- **`ta` command** — run any indicator on any ticker
- **`signal` command** — automated buy/sell signals with cat confidence rating
- **`pattern` command** — candlestick pattern recognition (doji, hammer, engulfing, morning star)
- **Econometrics engine** — OLS regression, Granger causality, Cointegration, CAPM, Correlation
- **`ols`, `granger`, `coint`, `capm`, `risk`, `correl` commands**
- **`catsentiment` command** — AI market sentiment with cat verdict

### 🧠 Terminal — Cat Takes Over the UI

- **`replay` command** — time-travel replay of any market day, animated tick-by-tick
- **`dashboard` command** — visual split-panel dashboard (indices, portfolio, terminal)
- **`revenue` command** — full revenue tracking with projections
- **`status` command** — personal dashboard (tier, tuna, cat companion, streaks)
- **`daily` command** — login streak rewards (7/14/30 day milestones)
- **`challenges` command** — gamified challenges with tuna rewards
- **`achievements` command** — 26 achievements, 5 rarities, 10 ranks
- **`journal` command** — trading journal with mood tracking
- **Cats, miau, joke, purr** — 4 new cat commands
- **Persistent cat companion** — follows you through the terminal
- **Cat sounds via WebAudio** — meow, purr, chirp, hiss actually play through speakers

### 📊 Data — Cat Devours the Markets

- **Corporate bonds provider** — yields by rating (AAA→CCC) via FRED
- **Treasury yield curve** — full curve charting
- **Mortgage rates** — 30yr, 15yr, 5/1 ARM
- **Central bank rates** — EFFR, SOFR, IORB
- **ETF sector performance**
- **Market indices** — S&P 500, NASDAQ, DOW, FTSE, NIKKEI, DAX
- **Global bonds, commodities, derivatives**
- **Tuna Price Index** — cat food basket tracking

### 🐱 Marketing — Cat Goes Viral

- **Bloomberg vs Miau comparison** — full feature table on ecosystem site + docs
- **Go-live checklist** — `docs/HOOOMAN HOW TO EARN CASH.md`
- **Go-live health check** — `scripts/go-live.sh`
- **Pitch decks** — English + German (docs/PITCH.md, docs/PITCH_DE.md)
- **Campaign files** — 7 platform-specific launch posts in `marketing/`
- **Meme templates, taglines, Gen Z manifesto**
- **Ecosystem site updated** — pricing, comparison, nav, CTAs

### 🛡️ Security — Cat Locks the Vault

- **Login rate limiting** — 5 failed attempts/min per IP
- **CSRF cookie httponly** — security hardening
- **Demo credentials removed from docs** — no more `admin`/`miau2026` in examples
- **K8s secrets cleaned** — real test keys replaced with placeholders
- **`.env` permissions fixed** — 600 (owner-only)

### 🐛 Fixes

- Registration endpoint fixed (DB password mismatch)
- OpenSky provider test now mocks HTTP (was hitting real API)
- FastAPI deprecation warnings fixed (`regex` → `pattern`)
- Missing `indices_api` import in main.py (broke test suite)
- Docker containers no longer crash-loop (npm/anonymous volume fix)
- Cat-governour script no longer conflicts with Docker services
- AGENT_LOG.md cleaned — 3100 lines of dog barks removed
- BARK.md reset to clean v3 format
- All boards synced — V6–V11 fully completed

---

## Summary

| Metric | v2.3.0 | v9.0.0 |
|--------|--------|--------|
| Commands | 50+ | **188** |
| API endpoints | 150+ | **515+** |
| Data providers | 25 | **37** |
| Frontend components | 20+ | **54** |
| Docker services | 10 | **14** |
| Backend tests | 136 | **260+** |
| Frontend tests | 19 | **93** |
| Cat interns | 0 | **10** 🐱 |
| Tuna reserve | 0 | **∞** 🐟 |
