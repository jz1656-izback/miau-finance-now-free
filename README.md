# Miau Finance - 🐱 Terminal-Based Financial Analytics Platform

[![Version](https://img.shields.io/badge/version-9.0--global--domination-brightgreen.svg)](https://github.com/LuZziD/cat-finance-analytics-shell-miau/releases)
[![License](https://img.shields.io/badge/license-OPEN%20SOURCE-brightgreen.svg)](LICENSE)
[![Free](https://img.shields.io/badge/price-FREE-ff6688?logo=heart)](https://github.com/LuZziD/cat-finance-analytics-shell-miau)
[![Cats](https://img.shields.io/badge/cats-🐱-ffcc00)](https://github.com/LuZziD/cat-finance-analytics-shell-miau)
[![Stars](https://img.shields.io/github/stars/LuZziD/cat-finance-analytics-shell-miau?style=social)](https://github.com/LuZziD/cat-finance-analytics-shell-miau)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev)
[![Tests](https://img.shields.io/badge/tests-88%20frontend%20passing-brightgreen?logo=vitest)](https://github.com/LuZziD/cat-finance-analytics-shell-miau/actions)
[![Courses](https://img.shields.io/badge/courses-230-success?logo=udemy)](https://localhost:5174)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Links](#-key-links)
- [Features](#features)
- [Apps & Services](#apps--services)
- [Authentication (Pawdenity)](#-authentication-pawdenity)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Available Commands](#available-commands)
- [API Documentation](#api-documentation)
- [Documentation](#documentation)
- [Changelog](#changelog)
- [License](#license)
[![Commands](https://img.shields.io/badge/commands-160%2B-blue?logo=terminal)](https://github.com/LuZziD/cat-finance-analytics-shell-miau/blob/dev/docs/api/COMMANDS.md)
[![Globe](https://img.shields.io/badge/V9-Global%20Domination-00e676?logo=three.js)](https://github.com/LuZziD/cat-finance-analytics-shell-miau/blob/dev/docs/roadmap/V9_BOARD.md)

## 🎉 MIAU IS FREE & OPEN SOURCE!

```
  /\_/\
 ( o.o )  😿 "miau is free..."
  > ^ <
 /_||_\
```

**No pawborghinis. No weird billionaires eating kittens. Just cats and charts.** 🐱📊

## Overview

**Miau Finance** is a FREE & OPEN SOURCE, Purrantir-inspired financial analytics platform with a cat-themed terminal UI. It combines real-time market data, portfolio optimization, risk analytics, and comprehensive financial analysis — all accessible through a beautiful green-on-dark terminal interface with CRT effects.

> _"Where cats trade stocks 🐱📈"_

---

```
  ╱|、
 (˚ˎ 。7
  |、˜〵
  じしˍ,)ノ    "Miau Finance: Where cats trade stocks
               and portfolios purr with delight."
```

```
 /\_/\     ╱|、
( o.o )   (˚ˎ 。7    "Cats don't have strategies.
 > ^ <    |、˜〵      They have vibes. We do both."
          じしˍ,)ノ
```

## 🔗 Key Links

| Link | URL |
|---|---|
| **GitHub Repo** | https://github.com/LuZziD/cat-finance-analytics-shell-miau |
| **Marketing Homepage** | http://localhost:3001 (after `cd miau-homepage && npm run dev`) |
| **MiauPapers (104 papers)** | http://localhost:3001/papers |
| **Blog** | http://localhost:3001/blog |
| **Terminal UI** | http://localhost:5173 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Docs (ReDoc)** | http://localhost:8000/redoc |
| **Log Viewer** | http://localhost:8000/logs-viewer |
| **Admin Panel** | http://localhost:8000/static/admin.html |
| **Grafana Dashboards** | http://localhost:3000 |
| **Docker Services** | :5173 Terminal · :5174 Education · :5175 MiauCorp · :5176 Marketing · :5180 Service Desk · :5190 Pawdenity Auth · :3001 Homepage · :8000 API · :3000 Grafana · :8088 Superset · :9001 MinIO · :9090 Prometheus |
| **ROADMAP** | https://github.com/LuZziD/cat-finance-analytics-shell-miau/blob/dev/ROADMAP.md |
| **CHANGELOG** | https://github.com/LuZziD/cat-finance-analytics-shell-miau/blob/dev/CHANGELOG.md |
| **AGENTS.md** | https://github.com/LuZziD/cat-finance-analytics-shell-miau/blob/dev/agents/AGENTS.md |
| **MiauPapers on GitHub** | https://github.com/LuZziD/cat-finance-analytics-shell-miau/blob/dev/docs/research/MIAUPAPERS.md |
| **SDK (Python)** | `/sdk/python/` |
| **SDK (curl examples)** | `/sdk/curl/` |
| **Docs** | `/docs/` — API, architecture, deployment, guides, security, compliance, research, releases, roadmap |
| **Kittyland** | `KITTYLAND.md` — Floating panel system for the terminal |
| **Miau DatChonk** | `CHONK.md` — Background data eating service |

## Features

### 📊 Data & Analytics
- 🗃️ **50+ Data Source Providers** — Finnhub, SecuritiesDB, HF Data, Mobula, EIA, IMF, BLS, Alpha Vantage, CoinGecko, FRED, Frankfurter, DumbStockAPI, Yahoo, DeFiLlama — unified DataSource pattern with health monitoring
- 📈 **Insider, Short, IPO, Ownership** — Real-time insider transactions, short interest, IPO calendar, institutional ownership via Finnhub
- 📊 **Risk Factors + Earnings Score + Fama-French** — AI-extracted 10-K risk factors, earnings call transparency (1-10), 5-factor loadings via SecuritiesDB
- 🔎 **Ticker Search** — Global ticker search across all exchanges via DumbStockAPI
- 🔬 **Alpha Vantage 48 Indicators** — RSI, MACD, BBANDS, SMA, EMA, STOCH, ADX, ATR, OBV, WILLR + 37 more
- 🏢 **SEC Filing + Earnings Analyzer** — 10-K/Q/8-K analysis with risk scores, section extraction, EPS surprise, sentiment
- ⛓️ **Options Chain** — Full options chain with Greeks and expiration dates
- 🕵️ **Insider Trading** — Form 4 insider transaction data
- 📡 **FRED Economic Data** — GDP, CPI, unemployment, Fed funds rate, Treasury yields
- 🌍 **Global Markets** — 40 international exchanges across Asia, Europe, LatAm, MEA with benchmark indices

### 🖥️ Terminal & Commands
- 📡 **Datavore Suite** — 50+ commands: insider, short, ipo, ticker, intraday, technicals, crosschain, macro, screener, cpi, employment, treasury, indicators, risk-factors, earnings-score, fama-french, passive-float, and more
- 🏦 **Catberg Bloomberg** — Bloomberg Terminal emulation with 30+ live-data panels (WEI, N, WCV, GPO, DES, FA...) powered by real APIs, not mock data
- 🧮 **15 Calculators** — DCA, compound, retirement, loan, margin, rebalance, benchmark, drawdown, montecarlo, blacklitterman, riskparity, pairtrade, optionspayoff, taxlot, correlation
- 🤖 **8 AI Commands** — aisummary, aisentiment, aiinsight, aireport, aiallocate, airisk, aitrade, aichooser
- 🐱 **Cat-Themed Terminal UI** — CRT scanlines, green phosphor glow, autocomplete, command history, ASCII cat art, chaos mode
- 💬 **Natural Language** — `ask "what are my top holdings?"` in plain English
- 🖥️ **Kittyland Panels** — Floating draggable panels. Type `price AAPL -p` to open any command output in a persistent, pinnable panel. [Read more](KITTYLAND.md)
- 🐱 **Miau DatChonk** — Background data eater. 45 cached entries refreshes every 30s. `price AAPL` is instant, `price AAPL -l` is live. [Read more](CHONK.md)

### 🗺️ Maps & Globes
- 🌍 **WorldMap** — Leaflet 2D map with 40+ exchanges, 50K+ company markers, boat/jet routes, ISS tracking, weather radar overlay
- 🌐 **MiauGlobe** — GPU-accelerated 3D WebGL globe (type `miaumap`) with company markers, trade route arcs, auto-rotation
- 🌧️ **Weather Overlay** — Live precipitation radar on WorldMap via RainViewer (free, no key)
- ❄️ **Company Sharding** — 7 continent-sharded JSON files instead of 11.5MB monolithic load — lazy-loaded on demand

### 📈 Trading & Portfolio
- 📊 **Real-Time Market Data** — Stocks, crypto, forex, commodities, treasury yields
- 📋 **Order Management** — Full OMS (5 order types) with paper trading, slippage, commission simulation
- 📈 **Strategy Engine** — 6 strategies (SMA, RSI, MACD, Bollinger, Mean Reversion, Momentum) with backtesting
- 🎯 **Trading Signals** — Technical indicator generation, multi-asset signals, SMA crossover backtesting
- 💱 **Multi-Currency** — Live FX rates, currency conversion, portfolio base currency (20 currencies)
- 🌐 **6 Broker Integrations** — Alpaca, Interactive Brokers, DEGIRO, Saxo, Rakuten, Zerodha

### 🔗 DeFi, Web3 & Enterprise
- 🔗 **DeFi & Web3** — WalletConnect v2, SIWE auth, encrypted keychain, 8 DeFi protocols (Uniswap, Aave, Curve, Lido, Yearn, Maker, Jupiter, Raydium)
- 🖼️ **NFT Portfolio** — Tracker, floor price monitoring, rarity scoring, collection valuation, marketplace API
- 🌐 **Cross-Chain Bridges** — LayerZero, Wormhole bridge monitoring
- 🏛️ **CBDC Support** — Digital Euro/Yuan/Dollar/Yen/Pound, multi-CBDC optimization, cross-CBDC settlement
- 🤝 **DAO Governance** — Miau DAO token, governor contract, treasury (multi-sig), proposal + voting UI
- 🏪 **P2P Marketplace** — Strategy NFT minting, licensing, reputation system, smart contract escrow

### 🤖 AI & AGI
- 🤖 **AI Advisor** — AI-powered portfolio analysis, market insights, risk assessment via GPT-4/Claude
- 🗺️ **AI Financial Analyst** — Fine-tuned financial LLM, RAG pipeline, multi-agent orchestrator, 21 agents
- 🧠 **AGI Finance Core** — Self-improving meta-learner, autonomous hypothesis generation, causal inference, evolutionary optimization
- 🛡️ **AGI Safety** — Hard guardrails, kill switch, confidence calibration, explainability (SHAP + NL)

### ⚛️ Quantum & Security
- ⚛️ **Quantum-Ready** — QUBO portfolio optimization, quantum annealing, VQE/QAOA hybrid, PQC (CRYSTALS-Kyber/Dilithium, FALCON)
- 🔐 **JWT Authentication** — Bearer token auth with RBAC, rate limiting, CORS, CSP, CSRF hardening
- 📦 **Python SDK + Plugin System** — SDK with market/portfolio/trading/AI modules, sandboxed plugins with 16 scoped permissions
- 📱 **Mobile PWA** — Responsive UI (320px+), touch gestures, offline mode, push notifications, installable PWA

---

## 🏢 Apps & Services

All standalone web apps share **Pawdenity** (port 5190) for single sign-on.

| App | Port | Description | Auth |
|-----|------|-------------|------|
| **🐱 Terminal UI** | 5173 | Main terminal — 200+ commands, real-time markets | `login` command |
| **🎓 Education Platform** | 5174 | 230 courses, 18 certifications | AuthModal / Pawdenity |
| **🏢 Miau Corp** | 5175 | Corporate ecosystem site, pricing, products | Pawdenity link |
| **📊 Marketing Dashboard** | 5176 | Analytics, campaigns, SEO, traffic | LoginForm / Pawdenity |
| **🚒 Service Desk** | 5180 | Ticket system, cat firefighters, system status | Login modal / Pawdenity |
| **🐾 Pawdenity** | 5190 | Central auth provider — one account all tools | Login/register form |
| **🚀 Landing Page** | 8080 | Cat rocket marketing page | Footer login link |
| **🔧 Admin Panel** | 8000/static/ | System monitor, provider health | Pawdenity / token paste |
| **📋 Log Viewer** | 8000/logs-viewer | Real-time log streaming | Pawdenity link |

> **One account:** Register via any app, login via Pawdenity. Token works everywhere.

## Changelog

> **Current: V9 — Global Domination Era 🐱🌍💰 (62 tasks, 10 epics, infinite tuna)**

### 🐱💨 V6 — Purrantir MiauGlobe Era (2026)

| Epic | What Shipped |
|------|-------------|
| **MiauGlobe Three.js** | globe.gl replaced with raw Three.js — 3000 star particles, atmosphere glow, auto-rotate, drag/zoom, resize handling |
| **WorldMap CDN Failover** | 3-tier CDN for Leaflet + MarkerCluster (unpkg → cdnjs → jsdelivr), 10s timeout, error-protected effects |
| **13 Calculator Commands** | `dca`, `compound`, `loan`, `retirement`, `margin`, `montecarlo`, `correlation`, `pairtrade`, `gas`, `blacklitterman`, `riskparity`, `benchmark`, `drawdown` + `fx`, `fxconvert` |
| **230 Education Courses** | Platform expanded from 118→230 courses across 60+ categories: calculators, Web3, quant, industry analysis, regional markets, professional development, Miau ecosystem |
| **Mining & Resources Layer** | 60 mines, 10 oil fields, 6 renewable sites rendered on MiauGlobe with commodity-color-coded markers |
| **Aliens Layer (+ Easter Egg)** | 20 UFO hotspots, type `x-files` to unlock, cat patrol markers near each UFO |
| **Cat Galaxy 3D** | Three.js galaxy with 3000 stars, 20 orbiting service nodes, nebula clouds, floating cat emojis |
| **Terminal Focus Fix** | Auto-focus on load, back/forward nav, tab switch, first click — service worker unregistration |
| **Cat Army Deployment** | `miaumap --catarmy` marches cats across the globe |
| **Flight Path Arcs** | Bezier curve trade routes between major airports on the globe |
| **Satellite Layer** | Live orbital position computation, ISS tracking, spy satellite mode |
| **Tutorial & Glossary** | 108-command tutorial (1325 lines), cat-themed financial glossary (269 lines) |

### 🐱💨 v2.3.0 — Datavore Edition + V4/V5

(Keeping the existing v2.3.0 / V4 / V5 sections below unchanged)

### 🟢 v2.0.0 — AGI Finance & Beyond

| Epic | What Shipped |
|------|-------------|
| **AGI Core** | Self-improving meta-learner, autonomous hypothesis generator, causal inference (do-calculus), evolutionary strategy optimization |
| **AGI Safety** | Hard guardrails, kill switch, confidence calibration, explainability (SHAP + NL), automated hypothesis backtesting |
| **Autonomous Wealth** | Goal self-discovery, sentient portfolio, tax optimization, cross-border arbitrage, financial singularity mode |
| **AGI Governance** | Oversight framework, human-in-the-loop, decision logging, trust scoring for autonomous agents |
| **AGI Frontend** | AGI dashboard (thoughts/strategies/safety), terminal commands, AGI API (10 endpoints) |
| **AGI Docs** | API docs, architecture docs, governance framework, safety guidelines |

### ✅ v1.9.0 — Quantum-Ready Finance

| Epic | What Shipped |
|------|-------------|
| **Post-Quantum Security** | CRYSTALS-Kyber KEM, CRYSTALS-Dilithium signatures, FALCON, hybrid crypto, PQC JWT, key management, liboqs Rust FFI |
| **Quantum Algorithms** | QUBO formulation (portfolio/TSP), quantum annealing (D-Wave + classical), VQE, QAOA, amplitude estimation for MC/risk/options |
| **Quantum API** | REST endpoints for QUBO solve, annealing, hybrid VQE/QAOA, portfolio optimization |
| **Quantum Frontend** | Quantum dashboard, terminal commands, K8s config (GPU/simulator nodes) |
| **PQC Migration** | Full migration guide, vulnerable algorithm audit, hybrid deployment strategy |

### ✅ v1.8.0 — Central Bank Digital Currencies

| Epic | What Shipped |
|------|-------------|
| **CBDC Integration** | Digital Euro/Yuan/Dollar/Yen/Pound, multi-CBDC portfolio optimization, yield optimization |
| **CBDC Services** | Real-time price tracker, adoption metrics, yield curves, allocation suggestions, rebalancing |
| **CBDC API** | GET /api/v1/cbdc — prices, info, adoption, yields, allocation |

### ✅ v1.7.0 — Gaming & Metaverse Finance

| Epic | What Shipped |
|------|-------------|
| **GameFi Portfolio** | Metaverse diversification analysis, NFT price alerts, cross-world arbitrage detection |
| **Gaming NFTs** | Gaming NFT portfolio + rental tracking, scholarship ROI calculator |

### ✅ v1.6.0 — Financial Education Platform

| Epic | What Shipped |
|------|-------------|
| **Education API** | 10 endpoints: courses, lessons, quizzes, progress, achievements, certificates |
| **Education Content** | Courses on investing, trading, DeFi, options, risk management |

### ✅ v1.5.0 — Personal AI Financial Analyst

| Epic | What Shipped |
|------|-------------|
| **AI Analyst Core** | Financial LLM inference, RAG pipeline, knowledge base, 4 research agents (data retrieval, portfolio, risk, market) |
| **Multi-Agent Orchestrator** | Agent coordination, task decomposition, result synthesis |
| **Deep Research** | Moat analysis, DCF generator, comps analysis, MA targets, short squeeze detection |
| **Personal Finance** | Health score, retirement simulator, college planner, insurance analysis, debt optimizer |

### ✅ v1.4.0 — Open Source Hedge Fund DAO

| Epic | What Shipped |
|------|-------------|
| **Fund Structure** | Fund NAV calculation, fee structure (management/performance/HWM), subscription/redemption API, compliance rules |
| **Community Trading** | Proposal workflow, weighted voting, execution engine, due diligence checklist, governance API |
| **Fund Transparency** | Real-time NAV tracking, holdings transparency, quarterly reports, investor portal, on-chain P&L verification |

### ✅ v1.3.0 — Miau Finance Network

| Epic | What Shipped |
|------|-------------|
| **P2P Marketplace** | Strategy NFT minting, licensing (4 tiers), reputation system, code audit, marketplace API |
| **DAO Governance** | MIAU token distribution (vesting/staking), proposal system, weighted voting, treasury management |
| **Frontend** | Marketplace browser, strategy detail view, proposal creation, voting UI |

### ✅ v1.1.0 — DeFi & Web3 Integration

| Epic | What Shipped |
|------|-------------|
| **WalletConnect** | SIWE auth (EIP-4361), encrypted keychain, EVM/Solana wallets, Ledger/Trezor support, WalletConnect v2 |
| **DeFi Protocols** | Uniswap, Aave, Curve, Lido, Yearn, Maker, Jupiter, Raydium, Marinade — swap, LP, lending, staking, vaults |
| **Yield Aggregator** | Best yields across protocols, impermanent loss calculator, gas estimator, MEV protection |
| **Cross-Chain Bridges** | LayerZero, Wormhole bridge monitoring |
| **NFT Services** | Portfolio tracker, floor price monitoring, rarity scoring, collection valuation, marketplace API |
| **DeFi Frontend** | WalletConnect QR + deep link, multi-chain balance display, DeFi portfolio dashboard |
| **NFT Frontend** | Gallery view, price chart (floor over time), portfolio heatmap |
| **DeFi Risk** | 7-factor risk scoring (decentralization, liquidity, audits, TVL, age, oracle, IL) |
| **Security Audit** | Full wallet security audit with 6 findings, prioritized recommendations |
| **JS SDK** | market.js, portfolio.js, trading.js modules |

### ✅ v1.0.0 — Autonomous Finance GA

| Epic | What Shipped |
|------|-------------|
| **Auto-Rebalance** | Portfolio drift detection, target allocation, rebalance plan generation |
| **Portfolio Export** | Export any portfolio to JSON/CSV/PDF |
| **Miau Score** | Composite score: Sharpe × ESG × diversity |
| **Cat Companion** | Animated cat reacting to P&L — purrs on gains, hides on losses |
| **Achievement System** | Unlockable achievements for milestones |
| **Catberg** | Bloomberg Terminal emulation — 41 function codes (WEI, N, WCV, GPO, DES, FA...), split-screen with real-time ticker bar, cat commentary, F1-F6 function keys |
| **Release Stabilization** | 280+ tests, security scan, load test (1k concurrent), Docker prod config, K8s GA manifests |

### ✅ v0.16.0 — Developer Platform

| Epic | What Shipped |
|------|-------------|
| **Python SDK** | Full async+sync SDK — market, portfolio, trading, AI modules with error handling, pagination |
| **curl Examples** | 14 shell scripts covering all 515+ endpoints |
| **SDK Autogen** | Auto-generate SDK modules from OpenAPI spec |
| **Plugin System** | Plugin spec + loader + 5 REST endpoints (install/list/run/remove/approve), example plugins (alert_handler, custom_strategy) |
| **Plugin Sandbox** | Restricted exec isolation with memory/time limits, API call proxy, blocked module list |
| **Plugin Permissions** | 16 scoped permissions, DB-backed approval/revocation flow, middleware enforcement |
| **API Versioning** | Semver header-based versioning, deprecation/sunset headers, changelog metadata |
| **Developer Logs** | Per-API-key request/response logging, timing, status distribution, key analytics |
| **Developer Docs** | SDK README, Plugin API guide, Developer Portal |

### ✅ v0.15.0 — Global Markets

| Epic | What Shipped |
|------|-------------|
| **MiauPapers** | 1012-line whitepaper collection — 10 short papers + 1 long manifesto, 20 hidden cat joke footnotes |
| **Investment Banking** | DCF valuation, WACC calculation, Comparable Company Analysis, LBO model (`sheetz miau`) |
| **3D World Globe** | WebGL 3D globe with country polygons, market points, animated arcs, data panels (`map` command) |
| **Correlation Matrix** | SVG heatmap with color-coded cells, hover tooltips, color legend (`correlation` command) |
| **Benchmark Comparison** | Recharts overlay chart (ticker vs SPY), alpha/beta/tracking error/correlation metrics (`benchmark` command) |
| **Map Legend** | Collapsible legend panel — region colors, market type icons, change color coding |
| **Scenario Analysis** | 6-scenario stress test (bear, mild, base, bull, melt-up, black swan), beta-weighted shocks |
| **Dividend Calendar** | Dividend yield, payout ratio, ex-date, projected income, multi-ticker calendar |
| **Rolling Metrics** | Rolling 12mo Sharpe ratio, volatility, beta with 20-period history |
| **Sector Peers** | 10→41 industry groups (AI, biotech, fintech, gaming, clean energy, REITs, etc.) |
| **Admin Dashboard** | Organization admin — team members, settings, billing info, API usage stats |

### ✅ v0.12.0 — Enterprise & Compliance

| Epic | What Shipped |
|------|-------------|
| **Tier Middleware** | Tier-gated rate limits for billing, API keys, and webhooks |
| **Audit Log Export** | CSV/JSON export with filters by action, date range, user |
| **SSO Foundation** | OAuth2/OIDC configuration middleware |
| **API Key Limits** | Per-key rate limit enforcement with usage tracking |
| **Invoice PDF** | PDF invoice generation with reportlab + download endpoint |
| **Usage Tracking** | Per-key request counting, data transfer metering, daily aggregation |
| **Migration Fixes** | Linearized migration chain, g0/g1 parallel head resolution |

### ✅ v0.12.0 — Data Monetization

| Epic | What Shipped |
|------|-------------|
| **Billing & Stripe** | Subscriptions (free/pro/enterprise), Stripe checkout/webhook, pricing UI, tier-based rate limits |
| **API Platform** | API key CRUD, developer dashboard, webhook management, usage tracking |
| **Enterprise** | API key auth middleware, invoice generation, auto-topup, billing cron |

### ✅ v0.11.0 — Social & Community MVP

| Epic | What Shipped |
|------|-------------|
| **Portfolio Sharing** | Public share links, leaderboards (weekly/monthly/all-time), follower system |
| **Activity Feed** | Real-time social feed, threaded comments, reputation badges |

### ✅ v0.10.0 — Mobile & PWA

| Epic | What Shipped |
|------|-------------|
| **Responsive UI** | Terminal at 320px-1024px, touch gestures, dark mode, accessibility score > 90 |
| **PWA** | Installable app, service worker, offline mode, push notifications, WhatsApp/Telegram bots |

### ✅ v0.9.5 — Advanced Trading

| Epic | What Shipped |
|------|-------------|
| **Order Management** | Full OMS (5 order types), paper trading with slippage/commissions |
| **Strategy Engine** | 6 strategies (SMA, RSI, MACD, Bollinger, Mean Reversion, Momentum), advanced backtesting, walk-forward optimization |
| **Broker Integration** | Alpaca Markets connector, Interactive Brokers stub |

### ✅ v0.9.0 — Intelligence & Scale

| Epic | What Shipped |
|------|-------------|
| **AI Advisor** | Portfolio analysis, market insights, risk assessment via GPT-4/Claude, natural language queries (`ask "what are my top holdings?"`) |
| **NLQ Parser** | Intent-to-endpoint mapping, regex fallback, streaming responses |
| **Multi-User Workspaces** | User/Team/Workspace models, RBAC (admin/user/readonly), activity logs, portfolio sharing |
| **Rust Analytics** | Anomaly detection (z-score, isolation forest, rolling stats), tokenizer, PyO3 bindings |
| **Data Quality** | Async gather for batch tickers, semaphore concurrency, outlier detection, retry with jitter |
| **Earnings Prediction** | Historical data collector, feature builder, model training pipeline, persistence |

### ✅ v0.8.0 — Expansion (Phases 6)

| Epic | What Shipped |
|------|-------------|
| **Rust Engine** | PyO3 Monte Carlo GBM, portfolio optimization, risk metrics, OLS regression |
| **Portfolio Attribution** | Brinson sector decomposition, per-security contribution, Fama-French factor attribution |
| **Regime Detection** | HMM with Rust-accelerated forward-backward, Viterbi decoding, 3 regime states |
| **Factor Analysis** | Fama-French 3/5-factor models, Ken French data library, sector exposure |
| **Pairs Trading** | Cointegration detection (ADF test), z-score signals, spread analysis |
| **Alert System** | Price/performance/risk alerts, multi-channel (email/SMS/push/in-app), cooldown |
| **Watchlist** | Multi-watchlist management, real-time price context, per-user defaults |
| **CI/CD Pipeline** | GitHub Actions: security audit, quality gates, tests, staging/prod deploy |
| **Security Hardening** | CSP, HSTS, CSRF, audit logging, request limits, XSS sanitization, JWT hardening |
| **Documentation** | 12 docs: API, COMMANDS, ARCHITECTURE, SECURITY, TUTORIAL, CONTRIBUTING, DEVELOPER, DESIGN, GLOSSARY, JOKES, PWA, FIX_LOG |

### ✅ v0.5.0 — Production (Phase 5)

| Epic | What Shipped |
|------|-------------|
| **Docker Compose** | 9 services (postgres, minio, redis, superset, prometheus, grafana, backend, frontend, education) |
| **JWT Authentication** | Token-based auth, refresh tokens, bcrypt hashing |
| **Rate Limiting** | Redis sliding window per IP with in-memory fallback, 429 + Retry-After |
| **Kubernetes** | HPA (2-10 replicas), PDB, TLS cert-manager, Ingress |
| **Prometheus + Grafana** | Metrics collection, 6 dashboards, request counters, duration histograms |

### ✅ v0.1.0–v0.4.0 — Foundation (Phases 1-4)

| Phase | Key Deliverables |
|-------|-----------------|
| **4** | Split terminal (tmux-style), sparkline charts, heatmap (3 modes), 3D globe, cat loaders |
| **3** | Monte Carlo GBM, Black-Litterman optimizer, VaR/CVaR, Options Greeks, trading signals |
| **2** | SEC EDGAR parser, FRED economic data, options chains, insider trading, news aggregation |
| **1** | Terminal UI with CRT theme, live market data, portfolio tracking, world map, auth |

---

## Quick Start

### Prerequisites

- Docker and Docker Compose v2
- Git
- Node.js 18+ (for frontend dev without Docker)
- Python 3.11+ (for backend dev without Docker)

### Using Docker (Recommended)

```bash
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git miau-finance
cd miau-finance
docker compose up -d
```

Wait for all services to become healthy (30–60s first time). Then access:

| Service | URL | Credentials |
|---|---|---|
| **Miau Terminal UI** | http://localhost:5173 | — |
| **REST API + Docs** | http://localhost:8000/docs | — |
| **Marketing Homepage** | http://localhost:3001 | — |
| **MiauPapers (104 papers)** | http://localhost:3001/papers | — |
| **Blog** | http://localhost:3001/blog | — |
| **Cube.js** | http://localhost:4000 | — |
| **Superset** | http://localhost:8088 | admin / admin |
| **Airflow** | http://localhost:8080 | admin / admin |
| **MinIO Console** | http://localhost:9001 | miau_admin / miau_secret |
| **Grafana** | http://localhost:3000 | admin / admin |
| **Log Viewer** | http://localhost:8000/logs-viewer | — |
| **Cat Galaxy** | http://localhost:5181 | — |
| **Admin Panel** | http://localhost:8000/static/admin.html | — |

### Without Docker

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Quick Commands

```bash
# Clone and start
git clone <repo-url> miau-finance && cd miau-finance
make up

# Seed sample data
make seed

# View logs
make logs

# Rebuild after changes
make rebuild
```

---

## Available Commands

| Command | Description |
|---|---|
| `price <ticker>` | Live price and change with sparkline |
| `chart <ticker>` | ASCII candlestick chart |
| `sparkline <t>...` | Compact sparklines for multiple tickers |
| `crypto` | Bitcoin price and top cryptos |
| `cryptomkt` | Crypto market overview |
| `cryptohist <coin>` | Crypto historical chart |
| `cryptotop <n>` | Top N cryptocurrencies |
| `fear` | Fear & Greed index |
| `forex` | Forex exchange rates |
| `sectors` | Sector performance |
| `movers` | Market gainers and losers |
| `commodities` | Gold, oil, silver prices |
| `treasury` | US Treasury yields |
| `breadth` | Market breadth (S&P, VIX, etc.) |
| `indicators` | Market indicators |
| `portfolios` | List all portfolios |
| `portfolio <id>` | Portfolio details and positions |
| `positions <id>` | Position breakdown |
| `trades` | Recent trades |
| `signals <ticker>` | Technical trading signals |
| `multisig <t1,t2>` | Multi-asset signals |
| `backtest <ticker>` | SMA crossover backtest |
| `optimize <tickers>` | Max Sharpe portfolio optimization |
| `minvar <tickers>` | Min variance portfolio |
| `eqweight <tickers>` | Equal weight portfolio |
| `risk <ticker>` | Comprehensive risk report |
| `var <ticker>` | Value at Risk |
| `beta <ticker>` | Beta vs market |
| `stress <ticker>` | Stress test scenarios |
| `greeks` | Options Greeks calculator |
| `correlation` | Visual correlation matrix heatmap (SVG) |
| `benchmark <ticker>` | Benchmark comparison vs SPY (chart + alpha/beta/tracking error) |
| `scenario <ticker>` | 6-scenario stress test (bear, bull, black swan) |
| `dividends <ticker>` | Dividend yield, payout ratio, ex-date, projected income |
| `rolling <ticker>` | Rolling Sharpe, beta, volatility (12mo window, 20-period chart) |
| `insider <ticker>` | Insider transactions, net buy/sell ratio |
| `short <ticker>` | Short interest, % float, days to cover |
| `ipo` | IPO calendar with filings, pricing, dates |
| `ownership <ticker>` | Institutional ownership, top holders |
| `ticker <query>` | Search tickers globally |
| `intraday <t> [i]` | Intraday OHLCV with sparkline |
| `technicals <t> [i]` | Technical indicators (RSI, MACD, SMA, etc.) |
| `crosschain` | Cross-chain bridge volumes |
| `macro <country>` | Macro dashboard (GDP, inflation, rates, debt) |
| `screener` | Stock screener by sector/price/market-cap |
| `cpi [country]` | Consumer Price Index YoY |
| `employment` | Employment data (nonfarm, unemployment) |
| `indicators` | 20+ economic indicators |
| `risk-factors <t>` | AI-extracted 10-K risk factor word count |
| `earnings-score <t>` | Earnings call transparency score (1-10) |
| `fama-french <t>` | Fama-French 5-factor loadings |
| `passive-float <t>` | % trapped in passive ETFs |
| `quanthealth <t>` | Piotroski F-Score (0-9), Altman Z, Beneish M-Score |
| `fairvalue <t>` | DCF fair value with upside/downside |
| `dca <amt> [p] [y] [r%]` | DCA backtest with CAGR |
| `compound <p> <r%> [y]` | Compound interest schedule |
| `loan <amt> <r%> [yrs]` | Loan amortization table |
| `retirement <a> <s> <m>` | Retirement projection |
| `riskparity <t1,t2>` | Risk parity portfolio weights |
| `famanch <ticker>` | Fama-French 5-factor loadings |
| `blacklitterman <t1,t2>` | Black-Litterman portfolio model |
| `sheetz miau -dcf <t>` | DCF valuation model |
| `sheetz miau -wacc <t>` | WACC calculation |
| `sheetz miau -comps <t>` | Comparable company analysis |
| `sheetz miau -lbo <t>` | LBO model |
| `sheetz miau -all <t>` | Run all 4 models sequentially |
| `fundamentals <t>` | Company financials overview |
| `earnings <ticker>` | Earnings calendar |
| `news <ticker>` | Company news |
| `marketnews` | Market news feed |
| `newsbatch <tickers>` | Batch news for multiple tickers |
| `search <query>` | Full-text search |
| `summary` | Platform summary stats |
| `ontypes` | List ontology types |
| `onobjects` | List ontology objects |
| `instruments` | List all instruments |
| `instypes` | List instrument types |
| `sectorslist` | List all sectors |
| `pnl [days] [id]` | P&L time series |
| `performance <id>` | Instrument performance |
| `optperf` | Optimizer performance metrics |
| `anportfolio <id>` | Portfolio analytics (JSON) |
| `anrisk <id>` | Portfolio risk analytics (JSON) |
| `pipelines` | List pipeline runs |
| `calc pnl` | Calculate P&L from positions |
| `all` | Comprehensive data dump |
| `map` | Toggle Leaflet 2D map |
| `miaumap` | Toggle 3D GPU globe (WebGL, drag to rotate, click markers) |
| `map2d` | Toggle Canvas 2D globe |
| `back` | Back to terminal |
| `cat` | Print a cat + random joke |
| `joke` | Tell a cat/finance joke |
| `cats` | Cat army |
| `help` | Show help |
| `clear` | Clear screen |

Type `help` in the terminal for the full command reference.

---




























---

## Project Structure

```
miau-finance/
├── Makefile                 # Convenience commands
├── netlify.toml              # Landing page deploy config
├── .env                     # Environment configuration
│
├── apps/                    # Standalone web applications
│   ├── ecosystem-site/      # Miau Corp — corporate/ecosystem landing page (5175)
│   ├── education-platform/  # Miau Learning — 230 courses, 18 certifications (5174)
│   ├── marketing-dashboard/ # Marketing analytics, campaigns, SEO, traffic (5176)
│   ├── service-desk/        # Miau Fire Brigade — ticket system, support (5180)
│   ├── auth/                # Pawdenity — central auth provider (5190)
│   └── landing-page/        # Cat rocket landing page (8080)
│
├── backend/                 # Python/FastAPI backend
│   ├── app/
│   │   ├── api/             # REST API routes (70+ router modules)
│   │   │   ├── analytics/   # 20+ analytics modules
│   │   │   ├── network/     # P2P marketplace + governance
│   │   │   ├── defi/        # DeFi wallet + protocols
│   │   │   └── security/    # PQC crypto API
│   │   ├── middleware/      # 25+ middleware modules (auth, rate limit, PQC, etc.)
│   │   ├── services/        # Business logic (100+ service modules)
│   │   │   ├── ai/          # AI advisor, NLQ, AGI core
│   │   │   ├── analytics/   # Market data, risk, valuation, scenario
│   │   │   ├── brokers/     # Alpaca, IBKR, Saxo, DEGIRO, Rakuten, Zerodha
│   │   │   ├── defi/        # DeFi protocols, NFT, yield aggregation
│   │   │   ├── network/     # Strategy NFT, licensing, reputation
│   │   │   ├── quantum/     # QUBO, annealing, hybrid VQE/QAOA
│   │   │   ├── plugin/      # Plugin system
│   │   │   └── data_sources/# 40+ data providers
│   │   ├── models/          # SQLAlchemy models
│   │   └── schemas/         # Pydantic schemas
│   ├── alembic/             # DB migrations (18 migration files)
│   ├── tests/               # Python test suite (70+ test files)
│   └── rust_analytics/      # Rust PyO3 analytics engine
│
├── frontend/                # React/TypeScript terminal UI
│   ├── src/
│   │   ├── components/      # 75+ UI components
│   │   ├── locales/         # 9-language i18n
│   │   ├── lib/             # API client, 200+ commands, themes
│   │   └── pages/           # Dashboard, Portfolio, Map, etc.
│   ├── public/              # Globe textures, company datasets
│   └── tests/               # Frontend test suite
│
├── infra/                   # Infrastructure & operations
│   ├── docker/              # Docker Compose files (main, dev, prod)
│   │   ├── docker-compose.yml       # Main compose (12 services)
│   │   ├── docker-compose.dev.yml   # Dev profile (4 core services)
│   │   ├── docker-compose.prod.yml  # Production (PgBouncer, replicas)
│   │   └── docker-compose.override.yml
│   ├── k8s/                         # Kubernetes manifests
│   ├── postgres/init/               # SQL schema + seed data
│   ├── prometheus/                  # Prometheus config
│   ├── grafana/dashboards/          # 15+ Grafana dashboards
│   ├── cube/schema/                 # Cube.js data model
│   ├── superset/config/             # Superset configuration
│   ├── airflow/                     # Airflow DAG definitions
│   └── plugins/                     # Example plugins
│
├── sdk/                     # Client SDKs (Python, JavaScript, curl)
├── docs/                    # All documentation
│   ├── api/                 # API reference, commands, plugin API
│   ├── architecture/        # Architecture, design, backend, frontend
│   ├── deploy/              # Deployment, docker, on-premise
│   ├── guides/              # Tutorial, quickstart, FAQ, glossary
│   ├── product/             # Features, services, monetization
│   ├── security/            # Security, audit, PQC
│   ├── compliance/          # GDPR, SOC2, TOS, privacy
│   ├── research/            # Whitepapers, MiauPapers
│   ├── releases/            # Changelog, release notes
│   ├── roadmap/             # Version boards V3-V11
│   └── archive/             # Archived docs
│
├── config/                  # Shared configuration
│   ├── .env.example         # Environment template
│   ├── .env.go-live         # Go-live env template
│   ├── shared-design-tokens.css  # Design system tokens
│   └── .miau-ascii          # Cat ASCII art collection
│
├── scripts/                 # Utility scripts (install, deploy, SDK gen)
├── agents/                  # AI agent definitions & logs
├── marketing/               # Marketing copy (launch content, taglines)
│
├── README.md
├── CHANGELOG.md
├── ROADMAP.md
├── VERSION
└── LICENSE
```
├── docs/                    # 20+ docs (API, COMMANDS, ARCHITECTURE, SECURITY, i18n, SOC2, SDK, PLUGIN_API, etc.)
│   ├── ops/                 # Incident response playbook, rollback procedure
│   ├── security/            # PQC migration guide, wallet audit, defi audit
│   ├── legal/               # Fund structure docs
│   └── whitepaper/          # Quantum finance whitepaper
└── .github/workflows/       # CI/CD pipelines
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://miau:miau_secret@postgres:5432/miau` | Async PostgreSQL connection |
| `DATABASE_URL_SYNC` | `postgresql+psycopg2://miau:miau_secret@postgres:5432/miau` | Sync PostgreSQL connection |
| `MINIO_ENDPOINT` | `minio:9000` | MinIO server endpoint |
| `MINIO_ACCESS_KEY` | `miau_admin` | MinIO access key |
| `MINIO_SECRET_KEY` | `miau_secret` | MinIO secret key |
| `CUBEJS_API_URL` | `http://cube:4000` | Cube.js API URL |
| `CUBEJS_API_SECRET` | `cube_secret` | Cube.js API secret |
| `REDIS_URL` | `redis://redis:6379/0` | Redis connection URL |
| `SUPERSET_SECRET_KEY` | `superset_secret_key_change_me` | Superset Flask secret |
| `SECRET_KEY` | `miau_secret_key_change_me` | JWT signing secret |
| `DEMO_USERNAME` | `admin` | Demo login username |
| `DEMO_PASSWORD` | `your_password` | Login password (change in production) |

---

## 🐳 Docker Deployment — One Command, Three Platforms

The fastest way to get Miau Finance running on **Windows, Linux, or macOS**.

### Prerequisites

1. Install **Docker** on your platform:
   - **Windows**: [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/)
   - **macOS**: [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/) (Apple Silicon or Intel)
   - **Linux**: [Docker Engine](https://docs.docker.com/engine/install/) + [Docker Compose](https://docs.docker.com/compose/install/)

2. Verify Docker is running:
   ```bash
   docker --version
   docker compose version
   ```

### Quick Launch (All Platforms)

```bash
# 1. Clone the repo
git clone https://github.com/jz1656-izback/miau-finance-now-free.git
cd miau-finance-now-free

# 2. Start everything (Postgres + Redis + Backend + Frontend)
docker compose -f docker-compose.simple.yml up -d

# 3. Wait 30 seconds for services to start, then open:
#    → http://localhost:5173  (Miau Terminal)
#    → http://localhost:5174  (Education Platform)
#    → http://localhost:5175  (Ecosystem Site)
```

### Platform-Specific Setup

<details>
<summary><b>🪟 Windows</b></summary>

1. Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
2. Install [Git for Windows](https://git-scm.com/download/win)
3. Open **PowerShell** or **Command Prompt**:
   ```cmd
   git clone https://github.com/jz1656-izback/miau-finance-now-free.git
   cd miau-finance-now-free
   docker compose -f docker-compose.simple.yml up -d
   ```
4. Open http://localhost:5173 in your browser
5. Type `help` for commands, `login pawdmin` (password: miau2026)

**Troubleshooting Windows**:
- If port 5173 is in use: change the port in `docker-compose.simple.yml`
- If Docker Desktop won't start: enable WSL2 in Windows Features
- Firewall may ask for permission — allow Docker
</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y docker.io docker-compose-v2 git
sudo systemctl enable --now docker
sudo usermod -aG docker $USER  # Log out and back in after this

# Fedora
sudo dnf install -y docker docker-compose git
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# Clone and run
git clone https://github.com/jz1656-izback/miau-finance-now-free.git
cd miau-finance-now-free
docker compose -f docker-compose.simple.yml up -d
```

Open http://localhost:5173 — no sudo needed!
</details>

<details>
<summary><b>🍎 macOS</b></summary>

1. Install [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
2. Open **Terminal**:
   ```bash
   git clone https://github.com/jz1656-izback/miau-finance-now-free.git
   cd miau-finance-now-free
   docker compose -f docker-compose.simple.yml up -d
   ```
3. Open http://localhost:5173

**Apple Silicon (M1/M2/M3)**: Docker runs natively — no extra config needed.
</details>

### What Gets Deployed

| Service | Port | Description |
|---------|------|-------------|
| 🐱 **Terminal** | :5173 | Main trading terminal with 200+ commands |
| 📚 **Education** | :5174 | 230 courses, terminal practice |
| 🏢 **Ecosystem** | :5175 | Corporate landing page |
| ⚡ **Backend API** | :8000 | FastAPI with 548 endpoints |
| 🗄️ **PostgreSQL** | :5434 | Company database (79K+ companies) |
| 📦 **Redis** | :6379 | Caching & rate limiting |

### Post-Deployment

```bash
# Check if everything is running
docker compose -f docker-compose.simple.yml ps

# View logs
docker compose -f docker-compose.simple.yml logs -f backend

# Create admin user
docker compose -f docker-compose.simple.yml exec backend python -m app.seed_admin

# Stop everything
docker compose -f docker-compose.simple.yml down

# Stop and delete all data
docker compose -f docker-compose.simple.yml down -v
```

### Login

Open the terminal at http://localhost:5173 and type:
```
login pawdmin
```
Password: `miau2026`

Then explore the 200+ commands — type `help` to see them all! 🐱



---

## API Documentation

Full API reference available at:

- **Swagger UI**: http://localhost:8000/docs (when running)
- **ReDoc**: http://localhost:8000/redoc (when running)
- **Full Reference**: [`docs/API.md`](docs/API.md) — all 515+ endpoints documented

The API exposes **515+ endpoints** organized into:
- Platform (health, version)
- Authentication (JWT token + refresh)
- Ontology (types, objects, links)
- Instruments (list, detail, market data, sectors, types)
- Portfolios (list, detail, positions, trades, currency conversion, rebalance)
- Trades (list, detail)
- Search (full-text)
- Pipelines (ETL runs, P&L calculation)
- Analytics (summary, portfolio analytics, P&L timeseries, performance, FX P&L, scenario, dividends, rolling)
- Market Data (live, historical, crypto, forex, indicators, global markets)
- News (market, company, batch)
- Portfolio Optimizer (max Sharpe, min variance, equal weight, Black-Litterman, performance)
- Risk Analytics (VaR, beta, stress test, Greeks, comprehensive, rolling metrics)
- Trading Signals (generate, multi, backtest)
- Fundamentals (overview, income, balance sheet, cashflow, earnings, SEC filings, insider trades)
- Economics (commodities, treasury, breadth, correlation, gainers/losers, FRED data)
- Options Chain (chain + Greeks by expiration)
- Reports (PDF, Excel, CSV, valuation CSV export)
- Valuation (DCF, WACC, Comps, LBO)
- Currencies (list supported, convert, set portfolio base)
- ESG (company scores, portfolio score, screening)
- Carbon (company data, portfolio footprint)
- Green Finance (renewable energy ETFs, green bonds, sustainable funds)
- Developer (dashboard, API keys, webhooks, plugins, request logs)
- AI Advisor (portfolio analysis, market insights, risk assessment, NLQ)
- Workflows (multi-step agentic trading workflows)
- DeFi (WalletConnect, wallet balance, protocols, NFT portfolio, risk scoring)
- Network (P2P marketplace, strategy licensing, governance voting)
- Fund DAO (NAV, fees, proposals, voting, holdings, quarterly reports)
- Education (courses, lessons, quizzes, progress, certificates)
- Gaming & Metaverse (GameFi, NFT gaming, virtual land)
- CBDC (prices, info, adoption, yields, allocation)
- Quantum (portfolio, QUBO solve, hybrid VQE/QAOA, annealing)
- PQC (Kyber keygen, Dilithium keygen, FALCON keygen)
- AGI (hypotheses, status, executor, risk manager, compliance)
- WebSocket (real-time prices)

---

## Documentation

| Document | Description |
|----------|-------------|
| [`docs/api/API.md`](docs/api/API.md) | Complete API reference (515+ endpoints, request/response examples) |
| [`docs/api/COMMANDS.md`](docs/api/COMMANDS.md) | Terminal command reference (160+ commands, output examples) |
| [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md) | System architecture, data flows, scaling |
| [`docs/guides/TUTORIAL.md`](docs/guides/TUTORIAL.md) | Hands-on getting started walkthrough |
| [`docs/guides/CONTRIBUTING.md`](docs/guides/CONTRIBUTING.md) | Contributor guide, PR workflow, code conventions |
| [`docs/guides/DEVELOPER.md`](docs/guides/DEVELOPER.md) | Internal developer guide: add endpoints, commands, components |
| [`docs/guides/AUTH.md`](docs/guides/AUTH.md) | Authentication guide — Pawdenity, login, cross-app SSO |
| [`docs/guides/SERVICE_DESK.md`](docs/guides/SERVICE_DESK.md) | Service Desk usage — tickets, firefighters, FAQ |
| [`docs/security/SECURITY.md`](docs/security/SECURITY.md) | Security architecture: auth, rate limiting, CORS, threat model |
| [`docs/guides/GLOSSARY.md`](docs/guides/GLOSSARY.md) | Cat-themed financial glossary for humans and felines |
| [`docs/architecture/DESIGN.md`](docs/architecture/DESIGN.md) | Design system — colors, typography, CRT effects, animations, a11y |
| [`docs/compliance/SOC2.md`](docs/compliance/SOC2.md) | SOC 2 compliance — TSC mapping, controls, evidence |
| [`docs/compliance/README.md`](docs/compliance/README.md) | BaFin/GDPR compliance — 12 documents (privacy, TOS, ISMS, IKS, AML) |
| [`docs/api/PLUGIN_API.md`](docs/api/PLUGIN_API.md) | Plugin development guide — spec, permissions, sandbox, examples |
| [`docs/guides/DEVELOPER_PORTAL.md`](docs/guides/DEVELOPER_PORTAL.md) | Developer portal — API versioning, rate limits, webhooks, SDKs, plugins |

---

## Authentication

All apps share a single auth system via **Pawdenity** — the cat identity provider.

**Superadmin (development):**
```
Username: pawdmin
Password: miau2026
```

**Login flow:**
1. Open **http://localhost:5190** or click "🐾 Pawdenity" on any app
2. Enter credentials or register a new account
3. Token is stored in `localStorage` as `miau_token`
4. All apps pick it up automatically via the broadcast relay

**API login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"pawdmin","password":"miau2026"}'
```

Use the returned `access_token` in subsequent requests:
```bash
curl http://localhost:8000/api/v1/portfolios \
  -H "Authorization: Bearer <token>"
```

**Reference:** [`docs/guides/AUTH.md`](docs/guides/AUTH.md) — full authentication guide.

---

## Contributing

We welcome contributors of all species (cats, humans, and those in between). See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for the full contributor guide including PR workflow, code conventions, commit style, and where to start.

Quick overview:
1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing`)
3. Follow the [cat-themed commit conventions](docs/CONTRIBUTING.md)
4. Push and open a Pull Request against `dev`
5. Tag `@qwen` for review

Please ensure your code passes linting and existing tests before submitting.

---

## 🐱 Made in Germany 🇩🇪

Handcrafted with 🐱 and ☕ in the heart of Europe.

## Support the Cats

If Miau Finance helps you trade better, learn faster, or just puts a smile on your face, you can feed the cats:

```
ETH:  0xfE7DBcd1D924C7D2Da93702199C05506F0629f98
BTC:  bc1qqzgaz3ey6nd8u8q9dgjuhfujgx936tqngdth9q
SOL:  8tHHBBGwitbiNSBjijcVWkMCpoYdddGgpPgnZkLJmH3t
```

Every tuna helps keep the servers purring. 🐟

## License

**OPEN SOURCE** · See [LICENSE](LICENSE)

---

---

---

## 🐱 Version History (Cat-Themed Changelog)

| Version | Code Name | Highlights |
|---------|-----------|------------|
| **v2.3.0** | *Datavore + V4/V5* | 🐱💨 50+ providers, Catberg, WorldMap, MiauGlobe, 515 endpoints, webhook alerts, PWA, Grafana dashboards, 729+ tests |
| **v2.1.0** | *Pawborghini Edition* | 💰 $116/$396 pricing, education platform, 120 courses, 18 certs, security audit |
| **v2.0.0** | *AGI Finance & Beyond* | 🧠 Self-improving AGI core, autonomous wealth management, causal inference, sentient portfolio, singularity mode with kill switch |
| **v1.9.0** | *Quantum-Ready Finance* | ⚛️ QUBO/quantum annealing/VQE/QAOA, CRYSTALS-Kyber/Dilithium/FALCON PQC, D-Wave integration, hybrid quantum-classical |
| **v1.8.0** | *Central Bank Digital Currencies* | 🏛️ CBDC integration — Digital Euro/Yuan/Dollar/Yen/Pound, multi-CBDC portfolio |
| **v1.7.0** | *Gaming & Metaverse* | 🎮 GameFi tokens, virtual land portfolio, NFT gaming, metaverse economy |
| **v1.6.0** | *Financial Education Platform* | 📚 Courses, lessons, quizzes, certificates — investing, trading, DeFi, options |
| **v1.5.0** | *AI Financial Analyst* | 🗺️ Financial LLM, RAG pipeline, 4 research agents, deep research, personal finance |
| **v1.4.0** | *Open Source Hedge Fund DAO* | 🤝 Miau DAO token, NAV/fees, proposal voting, execution engine, investor portal |
| **v1.3.0** | *Miau Finance Network* | 🏪 P2P strategy marketplace, DAO governance, MIAU token, weighted voting |
| **v1.1.0** | *DeFi & Web3* | 🔗 WalletConnect, SIWE auth, 8 DeFi protocols, NFT services, cross-chain bridges, risk scoring |
| **v0.17.0** | *Sustainability & ESG* | 📊 ESG scores, carbon tracking — invest with a clear conscience (and the cat's approval) |
| **v0.16.0** | *Developer Platform* | 📦 Python SDK, plugin system with sandbox & permissions, API versioning, developer portal |
| **v0.15.0** | *Global Markets* | 🌍 Multi-currency, 40 intl exchanges, 5 intl brokers, 8-language i18n, IBKR/Saxo/DEGIRO/Rakuten/Zerodha |
| **v0.13.0** | *AI-Native Terminal* | 🎤 Voice commands, AI autocomplete, multi-step agentic workflows |
| **v0.12.5** | *MiauPapers & Visual Polish* | 📚 Whitepaper collection, 3D globe, correlation matrix, benchmark comparison, IB toolkit, map legend |
| **v0.12.0** | *Data Monetization + Enterprise* | 💰 Stripe subscriptions, API keys, usage billing, SSO, audit export, tier middleware |
| **v0.11.0** | *Social & Community* | 👥 Portfolio sharing, activity feed, leaderboards, follows, badges, Telegram/WhatsApp bots |
| **v0.10.0** | *Mobile & PWA* | 📱 Responsive UI, touch gestures, offline mode, push notifications, installable PWA |
| **v0.9.5** | *Advanced Trading* | 📋 Order management, paper trading, strategy engine, broker integration |
| **v0.9.0** | *Intelligence Foundation* | 🤖 AI advisor, multi-user workspaces, anomaly detection, data quality |
| **v0.8.5** | *Hardening & Polish* | 🔒 JWT auth, rate limiting, CSRF, CORS, security audit fixes |
| **v0.8.0** | *The Big Meow* | 🎯 Terminal UI, ontology engine, 120+ REST endpoints, WebSocket streaming |

---

## 🌪️ Chaos Mode

This project contains a hidden `chaos` command in the terminal. Type `chaos` to toggle:
- 🐱 Random cat facts appearing during commands
- 📡 Unexplained market pings
- 🎰 Chaos wheel spins for +5% confidence boosts
- 😸 Walking cat animations
- ☣️ 15% chance of mayhem on every command

> *"Sometimes a little chaos pushes the project further."*
> — The Chaos Monkey, Miau Finance Lead Architect

---

## 🐱 Cat Facts for Investors

1. A group of cats is called a **clowder** — like a clowder of index funds
2. Cats sleep 12-16 hours/day — optimal for **long-term holding strategies**
3. A cat's nose print is unique — like a **portfolio fingerprint**
4. Cats have 32 muscles per ear — useful for **hearing market rumors**
5. The first cat in space was **Félicette** (1963) — the original **moon shot**
6. Miau Finance was named after a cat walking across a keyboard during a trading session
7. Cats sweat through their paw pads — the original **paper hands**
8. The world's richest cat has a net worth of ~€13M — better returns than most hedge funds

---

---

## 📓 Cat Trading Journal

Keep a trading journal right inside the terminal. Log your trades with mood tracking and see your emotional P&L.

```
miau@finance:~$ journal buy 10 AAPL --reason "felt bullish, cat approved" --mood 😸
✅ logged: BUY 10 AAPL @ $150.25
miau@finance:~$ journal
📓 Trading Journal (last 7 days)
────────────────────────────────────────
  Today   BUY  10 AAPL  $150.25  😸
  Yesterday  SELL  5 TSLA  $250.00  😿
  Last week  BUY  20 SPY  $480.00  😐
```

Features:
- Log buys/sells with free-text reason
- Mood tracking with emojis (😸😿😐😡🤯)
- Local storage — no DB needed
- Journal stats: win rate by mood, best trades by emotion
- "Cat approved" trades get bonus luck 🍀

---

## 😸 Cat-fessions of a Day Trader

```
  ╱|、
 (˚ˎ 。7     "I bought the dip. Then the dip dipped.
  |、˜〵      Then the dip dipped again.
  じしˍ,)ノ    Now I own the entire dip factory."
              — Whiskers, Portfolio Manager

  ╱|、
 (˚ˎ 。7     "My cat walked across my keyboard.
  |、˜〵      Somehow my portfolio is up 12%."
  じしˍ,)ノ    — Anonymous Day Trader

  ╱|、
 (˚ˎ 。7     "I asked Miau AI what to buy.
  |、˜〵      It said 'tuna futures.'"
  じしˍ,)ノ    — Satisfied Customer

  ╱|、
 (˚ˎ 。7     "I FOMO'd into DOGE at the top.
  |、˜〵      My cat hasn't looked at me since."
  じしˍ,)ノ    — Regretful Investor

  ╱|、
 (˚ˎ 。7     "The cat pushed 'sell all' with its paw.
  |、˜〵      Best trade I never made."
  じしˍ,)ノ    — Lucky Trader

  ╱|、
 (˚ˎ 。7     "I shorted my cat's favorite company.
  |、˜〵      Now the cat owns 51% of me."
  じしˍ,)ノ    — Hostile Takeover Victim

  ╱|、
 (˚ˎ 。7     "Diamond paws 💎🐾"
  |、˜〵      "Paper paws 📄🐾"
  じしˍ,)ノ    "Cat paws 🐱 — always land on green"

  ╱|、
 (˚ˎ 。7     "I diversified into catnip futures.
  |、˜〵      My cat is now my financial advisor."
  じしˍ,)ノ    — Going All In
```

---

## 🐱 Why Cats Are Better Than Hedge Funds

| Criteria | Cats | Hedge Funds |
|----------|------|-------------|
| Annual return on catnip investments | 📈 +infinity% | 📉 varies |
| Portfolio diversification | 9 lives = 9x diversification | Usually just 1x |
| Risk management | Always lands on feet | Sometimes lands in bankruptcy |
| CEO comp Purrs/hour | 😸 Unlimited | 💰 $50M+/year |
| Insider trading | Acceptable (they're cats) | Illegal |
| Fur color correlation with market | 100% correlated to treat frequency | Not statistically significant |
| Ability to predict recessions | Sleeps 16h/day = always prepared | Missed 2008, 2020, 2022 |
| Customer satisfaction | 🐱 10/10 would pet again | 😬 Mixed |

---

## 🏆 Accolades & Trophies

```
  ╱|、
 (˚ˎ 。7     "Best Cat-Themed Financial Analytics Platform"
  |、˜〵       — Definitely Not a Made-Up Award, 2026
  じしˍ,)ノ
  
  ╱|、
 (˚ˎ 。7     "Most Likely to Make You Say 'Meow' During Earnings"
  |、˜〵       — CNBC parody newsletter
  じしˍ,)ノ
```

---

## 🏆 v2.0.0 — The Cats Did It (All 27 Phases)

```
  ╱|、          ╱|、          ╱|、
 (˚ˎ 。7       (˚ˎ 。7       (˚ˎ 。7      "27 phases.
  |、˜〵        |、˜〵        |、˜〵       514+ microtasks.
  じしˍ,)ノ     じしˍ,)ノ     じしˍ,)ノ    320+ tests. 10 Docker containers.
                                          1 cat in charge of everything.
                                          From v0.1.0 Terminal MVP to v2.0.0 AGI.
                                          The cat is pleased.
                                          (The cat is never pleased.
                                          This is historic.)"
```

**Phases 1-27: v0.1.0 → v2.0.0**

| Phase | Version | Theme | Status |
|-------|---------|-------|--------|
| 1-10 | v0.1.0-v0.11.0 | Foundation + Intelligence + Trading + Mobile + Social | ✅ |
| 11-12 | v0.12.0-v0.13.0 | Monetization + Enterprise | ✅ |
| 12.5 | v0.13.0 | MiauPapers & Visual Polish | ✅ |
| 13 | v0.14.0 | AI-Native Terminal (Voice, Autocomplete, Workflows) | ✅ |
| 14 | v0.15.0 | Global Markets (Multi-Currency, Intl Exchanges, i18n) | ✅ |
| 15 | v0.16.0 | Developer Platform (SDK, Plugins, Developer Experience) | ✅ |
| 16 | v0.17.0 | Sustainability & ESG (ESG Scores, Carbon Tracking) | ✅ |
| 17 | v1.0.0 | Autonomous Finance GA | ✅ |
| 18 | v1.1.0 | DeFi & Web3 (WalletConnect, protocols, NFT) | ✅ |
| 19 | v1.2.0 | AI Hedge Fund (RL agent, ensemble ML, meta-learning) | ✅ |
| 20 | v1.3.0 | Miau Finance Network (P2P marketplace, DAO governance) | ✅ |
| 21 | v1.4.0 | Open Source Hedge Fund DAO (NAV, proposals, voting) | ✅ |
| 22 | v1.5.0 | Personal AI Financial Analyst (LLM, agents, deep research) | ✅ |
| 23 | v1.6.0 | Financial Education Platform (courses, quizzes) | ✅ |
| 24 | v1.7.0 | Gaming & Metaverse Finance | ✅ |
| 25 | v1.8.0 | Central Bank Digital Currencies | ✅ |
| 26 | v1.9.0 | Quantum-Ready Finance (QUBO, annealing, PQC) | ✅ |
| **27** | **v2.0.0** | **AGI Finance & Beyond** | **✅ Released** |

---

## 🌍 V6: Purrantir MiauGlobe Era (Current Sprint)

MiauGlobe has been transformed into a Purrantir-style global intelligence platform with **13 backend data providers** and **56/75 tasks complete**. The globe now features live tracking of:

| Layer | Provider | Data Points |
|-------|----------|-------------|
| **🏢 Companies** | `corporate.py` | 42 Fortune Global HQ locations |
| **✈️ Aviation** | `opensky.py` | Live ADS-B aircraft tracking |
| **🚢 Maritime** | `maritime.py` | 40 ports, 30 shipping lanes, ship positions |
| **🪖 Military** | `geopolitical.py` | 60 bases, 36 nuclear facilities, 10-country defense $ |
| **⛏️ Mining** | `mining.py` + `energy.py` | 50 mines, 41 oil fields, 32 renewable sites |
| **👽 Alien/UFO** | `alien.py` | 25 UFO sightings, 20 ancient mystery sites |
| **🛰️ Satellite** | `satellite.py` | 17 orbital objects with Keplerian positioning |
| **🚢 Cargo** | `cargo.py` | 10 FedEx/UPS/DHL hubs, 18 freight routes |
| **⚔️ Conflicts** | `conflict.py` | 25 active conflict zones |

**Controls:** `TAB` to rotate, scroll to zoom, click any data point for detail popup. Press `miaumap` in the terminal. Toggle layers via the toolbar buttons.

---

## ☕ Support the Developer

This project is maintained on a diet of coffee, cat treats, and sheer spite. If you'd like to contribute:

- **Star the repo** ⭐ (free, effective, causes dopamin release)
- **Pet a cat** 🐱 (not financial advice, but good for your health)
- **Tell a friend** 📣 ("hey, check out this weird cat trading thing")
- **Send memes** 🎭 (to the Issues tab, labeled `meme-request`)

---

*Built with 🐱 by traders who prefer purrs to CNBC*
*Made with 💚 and questionable financial decisions*
*Maintained by a distributed network of cats in hoodies*
*The cat says v2.0.0 is good. The cat is plotting something for v3.0.0.*
