# Miau Finance — Side Projects 🐱

> **v2.3.0 Datavore Edition**
> Ecosystem · Education · Marketing · SDK · Rust · Infra

---

## 1. 🌐 Ecosystem Site (`ecosystem-site/`)

**Port:** 5175 · **Stack:** Vanilla HTML/CSS/JS + Vite

Corporate landing page for "Miau Corp — The Cat Empire." A single-page marketing site with:
- Animated hero (floating cats, planets, fish, stars)
- 14 product cards (Terminal, Learning, SDK, IB, ESG, DeFi, AI, Quant, etc.)
- 12 cat cabinet members with modal bios
- Whitepaper browser with pagination + detail modals
- SDK code snippets
- Cookie banner, cursor trail, PWA manifest + service worker
- Analytics tracking via `/api/v1/marketing/track`

**Run:** `npx vite dev --port 5175`

---

## 2. 🎓 Education Platform (`education-platform/`)

**Port:** 5174 · **Stack:** React 18 + TypeScript + Vite 6 + Tailwind CSS

Interactive learning platform with 120+ finance courses:
- 18 certifications (CMA, CMT, CQF, CAI, CDS, CESG, Bagholder, etc.)
- 5 career tracks
- Course browser with filtering by category/difficulty/tier
- Interactive terminal simulator — practice real commands
- Quiz panel per lesson with scoring
- Free/Pro/Enterprise tier gating via auth
- Continue-learning resume (localStorage)
- API proxy to backend at `localhost:8000`

**Run:** `npx vite dev --port 5174`

---

## 3. 📊 Marketing Dashboard (`marketing-dashboard/`)

**Port:** 5176 · **Stack:** React 18 + TypeScript + Vite + Recharts + TanStack React Query + Framer Motion

Marketing analytics dashboard with 11 pages:
- **Dashboard** — overview KPIs with sparklines
- **Traffic** — visitor analytics, sources
- **Campaigns** — campaign management and ROI
- **SEO** — search performance tracking
- **Conversions** — funnel visualization
- **Realtime** — live event stream
- **Links** — link tracking and management
- **Experiments** — A/B test results with ExperimentCard
- **Reports** — report builder and export
- **Alerts** — marketing alert configuration
- **Settings** — dashboard configuration

Includes CatBackground component, GeoMap, FunnelChart, HourlyHeatmap. API proxy to `localhost:8000`.

**Run:** `npx vite dev --port 5176`

---

## 4. 🦀 Rust Analytics Engine (`backend/rust_analytics/`)

**Stack:** Rust 2021 + PyO3 0.23 + ndarray + maturin

High-performance Rust analytics exposed to Python via PyO3:
- **Monte Carlo** — GBM simulation with histogram bins (154 lines)
- **Portfolio** — efficient frontier, stats, evaluation (242 lines)
- **Risk** — historical VaR, beta, stress scenarios (168 lines)
- **Regime Detection** — HMM forward-backward, Viterbi (350 lines)
- **Pairs Trading** — cointegration, ADF test (230 lines)
- **Regression** — OLS regression (216 lines)
- **Anomaly Detection** — z-score, Isolation Forest, rolling stats (368 lines)
- **Tokenizer** — NLP tokenization (89 lines)
- **Strategy Robustness** — Monte Carlo testing (127 lines)

**Total:** 2,186 lines across 11 `.rs` files. Python fallback when Rust unavailable.

**Build:** `maturin develop` or `cargo build --release`

---

## 5. 🧊 Cube.js Analytics (`cube/`)

**Port:** 4000 · **Stack:** Cube.js + PostgreSQL

Headless analytics API providing pre-aggregated metrics:
- `schema/Instruments.js` — instrument dimensions/measures
- `schema/MarketData.js` — market data metrics
- `schema/PnL.js` — profit & loss
- `schema/Portfolios.js` — portfolio analytics
- `schema/Positions.js` — position tracking
- `schema/Trades.js` — trade analytics

**Run:** `docker compose up cube`

---

## 6. 📈 Grafana Dashboards (`grafana/`)

**Port:** 3000 · **Stack:** Grafana + Prometheus

13 provisioned monitoring dashboards:
| Dashboard | Focus |
|-----------|-------|
| `miau-monitoring.json` | Main infrastructure monitoring |
| `miau.json` | General platform metrics |
| `api-usage.json` | API request volume and latency |
| `developer.json` | Developer KPIs |
| `sdk.json` | SDK usage metrics |
| `forex.json` | Forex market data |
| `global_markets.json` | Global market indicators |
| `carbon.json` | Carbon tracking metrics |
| `esg.json` | ESG scoring metrics |
| `defi.json` | DeFi protocol metrics |
| `nft.json` | NFT market metrics |
| `notifications.json` | Notification delivery metrics |

Auto-provisioned via `dashboards/dashboard.yaml` with 30s refresh.

---

## 7. 📏 Prometheus (`prometheus/`)

**Port:** 9090 · **Stack:** Prometheus

Metrics scraping configuration:
- Scrapes `/metrics` on backend (`backend:8000`) every 15s
- Self-monitoring included
- Data source for all Grafana dashboards

**Run:** `docker compose up prometheus`

---

## 8. 📊 Apache Superset (`superset/`)

**Port:** 8088 · **Stack:** Apache Superset (Python/Flask)

BI platform configuration:
- SQLite database (override via `SUPERSET_DB_URI` env)
- Embedded Superset enabled
- Dashboard native filters + cross-filters
- Row limit: 5,000
- CSRF disabled (embedded use)
- Alert/report notifications in dry-run mode

**Run:** `docker compose up superset`

---

## 9. ☸️ Kubernetes Manifests (`k8s/`)

**Stack:** Kubernetes YAML + cert-manager

18 production-grade manifests for deploying all Miau services:
| Manifest | Purpose |
|----------|---------|
| `namespace.yaml` | `miau-finance` namespace |
| `deployment.yaml` | Backend API (2 replicas, rolling update) |
| `frontend.yaml` | Frontend deployment |
| `service.yaml` | Backend ClusterIP service |
| `configmap.yaml` | Environment configuration |
| `secret.yaml` | Encrypted secrets |
| `ingress.yaml` | TLS ingress routing |
| `certificate.yaml` | cert-manager TLS certificate |
| `hpa.yaml` | Horizontal autoscaler (2-10 replicas) |
| `pdb.yaml` | Pod disruption budget |
| `postgres.yaml` | PostgreSQL statefulset |
| `redis.yaml` | Redis deployment |
| `wallet.yaml` | Wallet service |
| `notifications.yaml` | Notifications service |
| `intl_brokers.yaml` | International brokers |
| `plugin_sandbox.yaml` | Plugin sandbox |
| `pwa.yaml` | PWA service |
| `quantum.yaml` | Quantum computing service |

**Deploy:** `kubectl apply -f k8s/`

---

## 10. 🔌 Plugins (`plugins/`)

**Stack:** Python (async, Miau Plugin API)

Two example plugins demonstrating the plugin system:

### Alert Handler (`alert_handler/main.py`)
- Hooks: `AFTER_MARKET_DATA`, `ON_ERROR`
- Detects price anomalies (>10% change)
- Logs alerts to `/tmp/miau_alerts.jsonl`

### Custom Strategy (`custom_strategy/main.py`)
- Hooks: `ON_ANALYTICS`, `BEFORE_ORDER`
- Generates buy/sell signals from RSI + SMA crossover
- Implements iceberg orders for large quantities

---

## 11. 🗄️ PostgreSQL Schema (`postgres/`)

**Stack:** PostgreSQL SQL

Database initialization scripts (767 lines):
| File | Lines | Purpose |
|------|-------|---------|
| `init/000_init.sql` | 1 | Create `airflow` database |
| `init/001_ontology.sql` | 318 | Ontology engine schema (types, objects, links, permissions) |
| `init/002_seed_ontology.sql` | 136 | Seed data: instrument types, trade states, entity types |
| `init/003_sample_data.sql` | 169 | Sample financial data for development |
| `init/004_watchlist.sql` | 22 | Watchlist schema with user association |
| `init/005_marketing_campaigns.sql` | 121 | Marketing campaign tracking tables |

---

## 12. 🛠️ Utility Scripts (`scripts/`)

**Stack:** Bash + Python 3

| Script | Purpose |
|--------|---------|
| `install.sh` | One-command install: clones repo, generates `.env` with 7+ secure secrets, starts all 10 Docker services |
| `gen_sdk.py` | Auto-generates Python async SDK methods and curl scripts from endpoint definitions (145 lines) |
| `agent-status.sh` | Dev workflow helper: checks git status, Docker health, backend health, pending messages (89 lines) |
| `decision.sh` | Agent coordination: proposes, records, and checks architectural decisions (82 lines) |

---

## 13. 📄 Static Assets (`static/`)

**Stack:** Vanilla JavaScript

- `tracker.js` — Client-side analytics beacon (35 lines)
  - Generates session ID (localStorage)
  - Tracks page views on load and SPA navigation
  - Captures UTM parameters, screen resolution, language, referrer
  - Supports conversion events via `data-track-conversion` attributes
  - Uses `navigator.sendBeacon` for reliable delivery

---

## 14. 🧪 Load Testing (`tests/`)

**Stack:** Python 3 + httpx + asyncio

- `load_test.py` — Async load testing script (231 lines)
  - Configurable concurrent users (default: 50), spawn rate, duration
  - Tests 4 critical endpoints: health, market live, market sectors, risk
  - Reports: total requests, success/fail, req/s, p50/p95/p99 latency
  - JWT auth token acquisition
  - Results saved to JSON file
  - Semaphore-based concurrency control

**Run:** `python tests/load_test.py --users 100 --duration 60`

---

## Network Overview

```
┌─────────────────────────────────────────────────────┐
│                    User Browser                      │
│  :5173 (Terminal)  :5174 (Education)  :5175 (Eco)  │
│  :5176 (Marketing Dashboard)                        │
└──────────┬──────────────────────────────┬───────────┘
           │ http (Vite proxy)            │
           ▼                              ▼
┌──────────────────┐           ┌─────────────────────┐
│   Backend :8000  │           │  Cube.js :4000       │
│   FastAPI + REST │           │  Analytics API       │
└────────┬─────────┘           └─────────────────────┘
         │
         ▼
┌──────────────────┐
│  PostgreSQL :5432 │
│  Redis :6379      │
│  MinIO :9000      │
└──────────────────┘
```

Monitoring: Grafana :3000 · Prometheus :9090 · Superset :8088
Infra: Airflow :8080 · K8s (production)
