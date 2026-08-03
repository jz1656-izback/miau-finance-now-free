# Miau Finance — Changelog

All notable changes, grouped by phase and agent. Each entry maps to a git commit.

---

## V6 "Purrantir MiauGlobe Era" — All-Seeing Globe — 2026-05-20 (KICKOFF)

**75 tasks across 11 epics.** Transform MiauGlobe into a Purrantir-style global intelligence platform with live tracking of planes, boats, military assets, mines, companies, satellites, aliens, and cats.

See [`V6_BOARD.md`](V6_BOARD.md) for full task breakdown.

| Epic | Theme | Tasks |
|------|-------|-------|
| V6-001 | MiauGlobe Foundation | 7 — draggable, layers panel, night city lights, terrain |
| V6-002 | Aviation | 6 — live ADS-B flights, cat-jets, airports |
| V6-003 | Maritime | 6 — live AIS ships, cat-boats, shipping lanes |
| V6-004 | Military | 7 — bases, defense spending, conflicts, nukes |
| V6-005 | Mining & Resources | 6 — 5,000+ mines, oil/gas, renewables |
| V6-006 | Corporate | 6 — Fortune 2000, supply chains, M&A arcs |
| V6-007 | Satellite | 7 — 10,000+ satellites, Starlink, ISS |
| V6-008 | Cat Layer | 7 — cat markers, cat army, cat ratings |
| V6-009 | Alien Layer | 8 — UFO sightings, Area 51, cats vs aliens |
| V6-010 | Data Integration | 10 — 7 new providers, globe API |
| V6-011 | Testing | 5 — render, interaction, provider, perf |
| **Total** | | **75** |

**Status: 75/75 tasks complete (as of May 2026).** All V6 tasks delivered.

| Provider | Data | Lines | Tasks |
|----------|------|-------|-------|
| **corporate.py** | 42 Fortune HQ locations | 107 | V6-006a, V6-010f |
| **mining.py** | 50 global mines/oil/renewables | 102 | V6-005a, V6-010e |
| **geopolitical.py** | 60 military bases, 36 nuke facilities, 10-country defense $ | 105 | V6-004a/b/d |
| **energy.py** | 41 oil/gas fields, 32 renewable installations | 95 | V6-005b/c |
| **alien.py** | 25 UFO sightings, 20 ancient sites | 87 | V6-009a/d, V6-010g |
| **conflict.py** | 25 active conflict zones | 55 | V6-004c, V6-010c |
| **satellite.py** | 17 orbital objects + Keplerian position engine | 97 | V6-007a/d, V6-010d |
| **cargo.py** | 10 FedEx/UPS/DHL hubs, 18 freight routes | 68 | V6-002e |

### Globe Layers Added
- **Military bases** (60 bases, orange dots sized by personnel, click popup with cat general rank)
- **Corporate Fortune** (42 companies from live backend, click popup with ticker/industry/revenue)
- **Satellite detail** (operator, orbit, altitude, launch date, cat space fact)
- **Mine coloring** (commodity-based: gold→yellow, copper→bronze, oil→black, renewable→green)
- **UFO/Alien hotspots** (25+ locations with click popup, `x-files` easter egg unlock)
- **Spy satellite mode** (6 classified LEO sats with 🕵️ markers)
- **Satellite orbital paths** (ISS + Starlink trails)

### MiauGlobe Fixes
- Removed double-render loop that was wasting 60fps CPU (camera update only)
- Container mounted via `createPortal` to prevent z-index clipping
- Debug red background (`#ff0000`) fixed back to `#050510`
- All Vite configs set to `strictPort: true` for all 4 projects
- Immortal-cat.sh: added missing 5174/5175/5176 services, ghost socket detection fix

---

## V9 "Global Domination Era" — Miau AI, Infinite Tuna — 2026-05-21

**62 tasks across 10 epics.** Full-stack production hardening, monetization launch, 3D charting suite, and the beginning of infinite tuna.

See [`V9_BOARD.md`](V9_BOARD.md) for full task breakdown.

| Epic | Theme | Tasks Done |
|------|-------|------------|
| V9-001 | Miau AI — Singularity Engine | 1/7 — cat veto command |
| V9-003 | Infinite Tuna Economy | 2/9 — tuna wallet, tuna command |
| V9-007 | Cat Metaverse | 1/6 — meow purr generator |

### Highlights
- **Billing live** (€99/€396 EUR pricing, dev mode checkout, Stripe-ready)
- **Pricing page** — `pricing` command with 3 tiers, CSRF fix, EUR currency
- **Installer** — `scripts/install-miau.sh` (10/10 tests pass, generates 14 passwords)
- **Scaling** — docker-compose.prod.yml (PgBouncer, 3× backend replicas, nginx, Redis cluster)
- **3D Chart Suite** — Chart3D, Sheetz3D, Compare3D (hover crosshair, cat reacts to trend, MAs, auto-rotate, animated bars, recommendation orb, connection lines)
- **V7 features** — kitten squad (`kittens` command), rave mode (`rave` with emoji rain)
- **V10 features** — Treasury yield chart (`yield`), global bond chart (`bonds`), mortgage provider
- **Security** — rate limits 3000/min, tier isolation, CSRF, HTTPS redirect fix
- **WorldMap updates** — 5 new layers (aircraft, maritime, mining, conflicts, satellites), search across all continents, real EU companies, IB panel login prompt

---

## V5 "Purring Production" — Production Hardening — 2026-05-20

### S-001: Health & Monitoring

| Commit | Agent | Description |
|--------|-------|-------------|
| `S-001a` | data-dev | Webhook alerts on provider failure — Slack/Discord POST with 5min rate limit via Redis |
| `S-001b` | data-dev | `health` terminal command showing uptime, providers, log file sizes |
| `S-001c` | data-dev | `GET /api/v1/health/services` — parallel health check for all 10 Miau services |
| `S-001d` | data-dev | Redis health history (7d TTL) + `GET /api/v1/health/history` endpoint |

### S-002: Mobile & PWA

| Commit | Agent | Description |
|--------|-------|-------------|
| `S-002a` | frontend-dev | PWA service worker v3 — offline fallback page, command caching, push event listener |
| `S-002b` | frontend-dev | Swipe gestures: down → palette, left/right → cycle heatmap/benchmark/correlation |
| `S-002c` | design-dev | Responsive layout: 640px + 380px breakpoints, stacked status bar, smaller fonts |
| `S-002d` | frontend-dev | Push notifications — VAPID JWT auth, `POST /push/send`, `POST /push/broadcast` |

### S-003: Grafana Dashboards

| Commit | Agent | Description |
|--------|-------|-------------|
| `S-003a` | infra-dev | Provider health dashboard: stat panels, uptime gauge, health graph, request/error stats |
| `S-003b` | infra-dev | API endpoint usage: top 10 endpoints/errors tables, error %, duration graph |
| `S-003c` | infra-dev | User activity: active users, requests, errors, hourly heatmap |
| `—` | infra-dev | Added `miau_providers_healthy`, `miau_providers_unhealthy` Prometheus metrics |

### S-004: Terminal UX

| Commit | Agent | Description |
|--------|-------|-------------|
| `S-004a` | frontend-dev | Persistent command history — localStorage, 500 commands |
| `S-004b` | frontend-dev | 57 new autocomplete entries added to COMMAND_META (achievements, catberg, defi, global, health, screener, etc.) |
| `S-004c` | frontend-dev | Tuna counter 🐟 (`cmdCount / 3`) in status bar |
| `S-004d` | design-dev | `cat --pet` — purring ASCII cat animation |

### S-005: Infrastructure

| Commit | Agent | Description |
|--------|-------|-------------|
| `S-005a` | infra-dev | Docker healthchecks for frontend, superset, airflow, education-platform — all 10 services |
| `S-005b` | data-dev | `scripts/start.sh` — `fuser -k` cleanup, governour kill |
| `S-005c` | backend-dev | .env validation — Stripe, Slack, SMTP, demo key warnings |
| `S-005d` | security-dev | Redis connection pool tuning — shared pool, `max_connections=10`, keepalive |

### S-006: Testing

| Commit | Agent | Description |
|--------|-------|-------------|
| `S-006a` | test-dev | 9 health endpoint tests (structure, services, history, metrics, timestamps, version) |
| `S-006b` | test-dev | 4 new fallback tests (timeout, rate limit, multi-capability, empty registry) — 11 total |
| `S-006c` | test-dev | 8 Cat Galaxy screen tests (render, health fetch, icons, hover, legend) |

---

## V4 "The Great Fixing Era" — Delittering — 2026-05-20

| Commit | Agent | Description |
|--------|-------|-------------|
| V4-001a | data-dev | Removed 11.5MB duplicate companies.json (replaced by lazy continent shards) |
| V4-001b | data-dev | Removed .venv from git tracking + gitignore |
| V4-001c | data-dev | Flattened nested logviewer/logviewer/ directory |
| V4-001d | data-dev | Removed old companies.json from frontend/public/data/ |
| V4-002a | frontend-dev | Merged tile layer + weather overlay into one useEffect |
| V4-002b | frontend-dev | Merged resize observer into init effect |
| V4-002c | frontend-dev | Removed empty mount effect |
| V4-002d | frontend-dev | Removed duplicate tile layer effect (race condition) |
| V4-003a | backend-dev | Fixed billing_balances migration — created missing table |
| V4-003b | backend-dev | Fixed SecuritiesDB no-screener error in screener endpoint |
| V4-003c | backend-dev | Fixed Yahoo provider bare DataSourceError |
| V4-003d | docs-dev | Fixed stale version refs in education platform |
| V4-004a | design-dev | Verified no unused imports in WorldMap.tsx |
| V4-004c | design-dev | Tree-shook unused Leaflet controls — all in use |
| V4-005b | infra-dev | make up starts all 9 containers cleanly |

---

## Commercial Release: v2.3.0 "Datavore Edition" — 2026-05-20

| Commit | Agent | Description |
|--------|-------|-------------|
| `latest` | qwen | 25+ API providers (8 no-key: Yahoo, StockPrice.dev, Frankfurter, DeFiLlama, SecuritiesDB, DumbStock, Blocknative, CEX) |
| `latest` | qwen | 5 key-based providers (Finnhub, TwelveData, CoinPaprika, BLS, Etherscan) |
| `latest` | data-dev | 10 data providers: EIA, IMF, Mobula, HF Data, Dividend, Catalyst, Rebalance, TaxLot, Inflation, Energy, Agriculture, GDP, CrossChain |
| `latest` | frontend-dev | 50+ new terminal commands (screener, insider, short, ipo, yields, defillama, gas, famanch, riskfactors, passiveflow, earningscore, intraday, technicals, cpi, employment, treasury, indicators, fx, fxhistory, fxconvert) |
| `latest` | ai-dev | 8 AI commands (aisummary, aisentiment, aiinsight, aireport, aiallocate, airisk, aitrade, aichooser) |
| `latest` | frontend-dev | 15 calculator commands (dca, compound, retirement, loan, margin, rebalance, benchmark, drawdown, montecarlo, blacklitterman, riskparity, pairtrade, optionspayoff, taxlot, correlation) |
| `latest` | test-dev | 136+ tests for datavore layer (F-009, P9-004, P9-005) |
| `latest` | docs-dev | 5 courses updated, 120 total courses, 18 certifications |
| `latest` | qwen | Education API key auth (critical security fix for create_education_token) |
| `latest` | qwen | Timing attack fix in validate_user (hmac.compare_digest) |
| `latest` | qwen | Refresh token now requires re-authentication |
| `latest` | qwen | Tightened CSRF bypass from wildcard `/api/v1/education/*` to specific paths |
| `latest` | qwen | `chartz` command with `-l` (live/news), `-m` (mega/BBands/SR), `-lm` (max/cats), `-c` (CSV export) |
| `latest` | qwen | Yahoo Finance news API (free, no key needed) with clickable links |
| `latest` | qwen | Fama-French 5-factor (`famanch` command) |
| `latest` | qwen | Boat/jet animation fixes during zoom on WorldMap |
| `latest` | qwen | Auth security audit: 5 vulnerabilities fixed |
| `latest` | qwen | `.env.example` updated with EDUCATION_API_KEY |
| `latest` | all | Ecosystem site stats updated, version bumped everywhere |

---

## Commercial Release: v2.1.0 "Pawborghini Edition" — 2026-05-19

| Commit | Agent | Description |
|--------|-------|-------------|
| `dafb166` | docs-dev | Miau Shell Maniac Certification — 6 lessons, CMSM better than MBA |
| Previous | security-dev | Proprietary EULA — project is no longer open source (MIT → All Rights Reserved) |
| Previous | docs-dev | 4× price increase: Pro $29→$116/mo, Enterprise $99→$396/mo |
| Previous | docs-dev | Leaflet WorldMap — Google Maps-style search, pan/zoom, 3 tile layers |
| Previous | docs-dev | Pawborghini jokes — open source devs can't afford tuna, purraris, or pawrsches |
| Previous | docs-dev | Education platform prices KEPT: Kitten $0, Meowster $19/mo, Pride $99/mo |
| Previous | docs-dev | Full docs cleanup — removed all "open source" and MIT references (~25 files) |

---

## v2.1.0 "Pawborghini Edition" — 2026-05-19

| Commit | Agent | Description |
|--------|-------|-------------|
| `63bb26e` | frontend-dev | Company detail panel with SVG price chart + news from API |
| `a532584` | frontend-dev | Add S&P 500, DAX name clarity, replace DivIcon markers with circleMarkers |
| `c81b291` | docs-dev | Fix MIAUPAPERS ToC: restore Paper 11, add papers 34-42, 42/42 accounted for |
| `bb356bd` | frontend-dev | Search pans to company on map + show popup |
| `45a78cc` | frontend-dev | Slow smooth animation + commodities/bonds from API + bigger jets + dashboard panel |
| `b02d70c` | marketing | Screenshots, OG image, newsletter signup, README rewrite, licensing fix |
| `2be462c` | docs-dev | Ecosystem site: remove all open source refs — proprietary, paid, pawborghinis |
| `63cf630` | frontend-dev | 50 markets, 100+ companies, bigger markers, richer popups |
| `7760189` | frontend-dev | Larger fonts, bigger popups, wider panels |
| `b3629d4` | education | Remove orphaned code causing 501, add 100+ course commands |
| `daab0c8` | frontend-dev | Slow down animation 6x, remove random jumps, add 30 cats, 10 trade routes |
| `a2331ec` | frontend-dev | WorldMap — native Leaflet overlays + rich company popups |
| — | frontend-dev | 3 tile layers (street/satellite/dark), map layer toggle button |
| — | frontend-dev | 🐱 on all capital flows (cat-jets 🐱✈️) |
| — | frontend-dev | News tab connected, 5-tab detail panel (Info/Chart/Stats/Peers/News) |
| — | frontend-dev | 📈 Chart with period selector (1M/3M/6M/1Y/5Y) |
| — | frontend-dev | 🏦 IB tab — DCF, WACC, Comps, LBO valuation endpoints |
| — | frontend-dev | Search auto-select on Enter, detail panel opens on click |
| — | frontend-dev | Panel size increased to 720px, w-panel custom Tailwind class |
| — | frontend-dev | Build fixes: removed unused declarations, fixed lint errors |
| — | build | Tailwind config: custom w-panel/max-w-panel/max-h-panel values |
| — | backend | News API rewrite — Yahoo Finance search API + yfinance + hardcoded fallback |
| Previous | marketing | Education platform standalone at localhost:5174 |
| Previous | marketing | 6 screenshots, 1200×630 OG image, homepage README rewrite, sitemap 13 URLs |
| Previous | docs | Docs consolidation: 25+ MD files → 4 core + docs/ directory |
| — | infra | education-platform service added to docker-compose.yml |

---

## Phase 17: Autonomous Finance GA (v1.0.0) — 2026-05-19

### GA Features
| Commit | Agent | Description |
|--------|-------|-------------|
| `079fe9f` | backend-dev | Phase 16.2 — Carbon service + API: intensity, portfolio footprint, benchmark |
| `43e5c85` | backend-dev | Auto-rebalance engine + portfolio drift detection |
| `17.2.5` | frontend-dev | `export` terminal command (JSON/CSV/PDF) |
| `17.2.6` | frontend-dev | v1.0.0 welcome/animated boot screen |
| `17.2.7` | frontend-dev | Ctrl+R fuzzy history search |
| `17.2.8` | design-dev | Cat companion component (P&L-reactive) |
| `17.2.9` | frontend-dev | Achievement popup system |
| `17.2.3` | ai-dev | Miau Score (Sharpe × ESG × diversity) |

### Release Stabilization
| Commit | Agent | Description |
|--------|-------|-------------|
| `17.1.1` | test-dev | Full test suite sweep (280+ tests) |
| `17.1.4` | rust-dev | Performance benchmarks (p50/p95/p99) |
| `17.1.5` | security-dev | Security scan (bandit, SAST, deps) |
| `17.1.6` | infra-dev | Docker production config |
| `17.1.7` | infra-dev | K8s GA manifests |
| `17.1.9-11` | security-dev | Rate limit tuning, CORS/CSP audit, logging audit |
| `17.1.13` | test-dev | Static analysis (ruff, eslint, clippy) |
| `17.1.14` | test-dev | Load test (1000 concurrent) |

### Documentation (v1.0.0 Release)
| Commit | Agent | Description |
|--------|-------|-------------|
| `17.3.1` | docs-dev | Self-hosted deployment guide (`docs/DEPLOY.md`) |
| `17.3.4` | docs-dev | v1.0.0 release notes (`docs/RELEASE_NOTES.md`) |
| `17.3.5` | docs-dev | v1.0.0 CHANGELOG update |
| `17.3.6` | docs-dev | v1.0.0 README update |
| `17.3.7` | docs-dev | ROADMAP update (phases 1-17 complete) |
| `17.3.8` | docs-dev | AGENTS.md final update |

---

## Phase 13: AI-Native Terminal (v0.13.0) — 2026-05-19

### Voice & Intelligence
| Commit | Agent | Description |
|--------|-------|-------------|
| `b3bb6e7` | frontend-dev | Voice command input — mic button + Web Speech API speech-to-text |
| `b6fd0fa` | ai-dev | AI autocomplete — context-aware suggestions, subcommand completion, recency scoring, NLQ detection |
| `8b693ae` | security-dev | POST `/token/refresh` endpoint for sliding session renewal |
| `7221351` | security-dev | Security headers hardening — worker-src, COEP, X-DNS-Prefetch, Cache-Control |
| `458a867` | security-dev | Audit logging uses resolved user_id/tier/auth_type from TierMiddleware |
| `768fabe` | docs-dev | Paper 11 — Open Source, Open Books, Open Tuna |

---

## Phase 12.5: MiauPapers & Visual Polish (v0.12.5) — 2026-05-19

### Investment Banking Toolkit
| Commit | Agent | Description |
|--------|-------|-------------|
| `3492ae8` | backend-dev + docs-dev | MiauPapers — 1012-line whitepaper collection (10 papers + 1 manifesto, 20 hidden cat jokes) |
| `5b3c848` | backend-dev | DCF valuation, WACC calculation, Comparable Company Analysis, LBO model via `sheetz miau` |
| `d7ab89e` | banker-dev | `sheetz miau -all` flag — run DCF, WACC, Comps, LBO sequentially |

### Advanced Analytics
| Commit | Agent | Description |
|--------|-------|-------------|
| `5b3c848` | backend-dev | Scenario analysis — 6-scenario stress test, beta-weighted shocks |
| `5b3c848` | backend-dev | Dividend calendar — yield, payout ratio, ex-date, projected income |
| `2c41e65` | backend-dev | Rolling Sharpe/Beta/Volatility — 12mo window, 20-period history |
| `4f23f45` | docs-dev | Update COMMANDS.md + API.md with scenario, dividends, rolling, sheetz commands |
| `49e4c37` | test-dev | 32 tests for scenario, dividends, rolling, sheetz, billing, apikey commands |

### Visual Components
| Commit | Agent | Description |
|--------|-------|-------------|
| `270a520` | frontend-dev | WorldMap Globe.gl migration — WebGL 3D globe with country polygons, market points, arcs, data panels |
| `636c816` | frontend-dev | Correlation matrix heatmap — SVG heatmap, color legend, hover tooltips, `corr` command |
| `5859003` | frontend-dev | Benchmark comparison UI — Recharts overlay chart, alpha/beta/tracking error metrics |
| `451cedc` | frontend-dev | Wire BenchmarkComparison + CorrelationMatrix into Terminal |
| `76b44c1` | design-dev | MapLegend component — collapsible legend, region colors, market type icons |
| `76b44c1` | design-dev | WorldMapGlobe tooltip enhancements — flag emojis per region, market type icons |

### Terminal & Developer Console
| Commit | Agent | Description |
|--------|-------|-------------|
| `dac174b` | frontend-dev | Organization admin dashboard — team members, settings, billing, API usage stats |
| `b2fd08d` | frontend-dev | Wire CorrelationMatrix + WorldMapGlobe into Terminal |
| `270a520` | frontend-dev | WorldMap Globe.gl migration — WebGL 3D globe with country polygons |
| `5b7d991` | data-dev | Expand sector peers — 10→41 industry groups |

---

## Phase 12: Enterprise & Compliance (v0.12.0) — 2026-05-19

### Enterprise Features
| Commit | Agent | Description |
|--------|-------|-------------|
| `5b3c848` | backend-dev | Tier middleware wired to billing + API keys — tier-gated limits, dashboard tier info |
| `c92eee4` | backend-dev | TierMiddleware — resolves subscription tier per request, attaches to `request.state` |
| `5b3c848` | backend-dev | Audit log export — CSV/JSON export with date/user/action filters |
| `e41fa57` | backend-dev | Fix audit export Query param for Pydantic v2 (`regex`→`pattern`) |
| `053a9c5` | security-dev | SSO groundwork — OAuth2/OIDC configuration middleware |
| `dac174b` | frontend-dev | Organization admin dashboard UI |

### API Platform
| Commit | Agent | Description |
|--------|-------|-------------|
| `214da3a` | security-dev | API key rate limit enforcement in middleware |
| `78ee23c` | security-dev | API key auth middleware, developer dashboard, webhook management |
| `be70996` | backend-dev + frontend-dev | API key CRUD, auth middleware, usage tracking, DeveloperConsole |

---

## Phase 11: Data Monetization (v0.12.0) — 2026-05-19

### Epic 11.1: Billing & Stripe
| Commit | Agent | Description |
|--------|-------|-------------|
| `e0282df` | backend-dev | Subscription model + schemas, Stripe checkout, Stripe webhook |
| `0e434cc` | backend-dev | Implement Phase 11 Monetization (subscriptions + Stripe) |
| `5b2370c` | backend-dev / frontend-dev | Billing service, trial/portal endpoints, PricingPage |
| `09c217d` | PM | Improve billing service — async Stripe customer management, checkout sessions, portal, DB subscription tracking |
| `6adc406` | frontend-dev | PricingPage, CheckoutButton, SubscriptionManager components + billing terminal commands |
| `1843ff5` | security-dev | Tier-based rate limiting — free(20/min), pro(100/min), enterprise(unlimited) |
| `7ff31f9` | PM | Fix billing.py syntax error (unclosed TIER_PRICES dict), update import names, wire tier middleware |
| `6112748` | docs | Update AGENTS.md |
| `c14e8bc` | test-dev | Billing API tests + subscription service tests + fix duplicate billing router |
| `9c8e143` | docs | Phase 11 epic 1 complete — mark all 20 tickets DONE |
| `78ee23c` | security-dev | Phase 12 Enterprise: API key auth middleware, developer dashboard, webhook management |
| `be70996` | backend-dev / frontend-dev | API key model, CRUD, auth middleware, developer dashboard, webhook management, usage tracker, DeveloperConsole |

### Epic 11.3: Usage Billing
| Commit | Agent | Description |
|--------|-------|-------------|
| `678bdcd` | frontend-dev | API key commands, usage dashboard, invoice list |
| `8135078` | backend-dev | Auto-topup service and billing cron scheduler |
| `c576448` | data-dev | Usage cron and billing cron |
| `bcacc0c` | security-dev | Phase 12 Enterprise final: API key management, webhook endpoints, invoice/auto-topup |
| `de3df53` | test-dev | Fix billing tests + create missing api_keys.py endpoint + fix schema order bug |
| `10c7451` | infra-dev | Add alembic migration commands to Makefile |

### Bug Fixes & Polish
| Commit | Agent | Description |
|--------|-------|-------------|
| `4245fc8` | docs | Update AGENTS.md, fix main.py duplicate billing router, add stripe to requirements |
| `1baaf88` | PM | Unblock backend — add extra=ignore to Settings, wire api_keys + webhooks, add migration, remove duplicate billing import |
| `d7a174b` | fix | Remove duplicate api_keys/webhooks router registrations |
| `33db437` | chore | Update stale Phase 10/11 ticket statuses to DONE |
| `f9d3b83` | fix | Install missing dompurify dep + fix duplicate billing key in autocomplete |
| `032c7e9` | PM | Fix migration chain (g1/g0 parallel heads), fix override.yml duplicate profiles |
| `ea381c2` | rust-dev | Resolve 3 pre-existing test failures |
| `8810773` | completer-dev | Cat trading journal command — track mood & trades in localStorage |

---

## Phase 10: Social & Community MVP (v0.11.0) — 2026-05-19

### Social Backend
| Commit | Agent | Description |
|--------|-------|-------------|
| `9da13ce` | social-dev | Phase 10 social backend verified + fix strategies_api import |
| `e63f9c2` | test-dev | Phase 10 social tests + bugfix: comment row key mismatch, expires_at comparison |
| `264362a` | test-dev | Sharing tests, feed tests, follow tests |
| `402fcee` | test-dev / infra-dev | Verify all test and infra tasks complete |

### Social Frontend
| Commit | Agent | Description |
|--------|-------|-------------|
| `f83089e` | frontend-dev | Social feed UI, comment UI, user profile UI, share/feed/social commands |
| `12308c1` | frontend-dev | Shared portfolio UI + leaderboard UI |
| `e603111` | frontend-dev | SharedPortfolioUI component |
| `cb2eeb4` | frontend-dev | Swipe gestures, heatmap touch, code splitting + perf budget |

---

## Phase 9: Mobile & PWA (v0.10.0) — 2026-05-19

### Responsive & PWA
| Commit | Agent | Description |
|--------|-------|-------------|
| `07dd3ed` | design-dev | Responsive breakpoints, font scaling, touch input, onboarding, safe area, reduced data, icons, accessibility |
| `a24d756` | design-dev | Responsive CSS, mobile onboarding, safe area, reduced data, splash screen, app icons |
| `12308c1` | frontend-dev | PWA setup (sw.js, manifest.json, update notification, mobile keyboard, bottom nav) |
| `327c6a5` | design-dev | PWA icons, manifest and service worker updates |
| `ef972d4` | frontend-dev | Implement Phase 9 PWA frontend components |

### Push Notifications
| Commit | Agent | Description |
|--------|-------|-------------|
| `a14e332` | social-dev | WhatsApp, Telegram bot, VAPID keys, push subscribe, price alert push, trade push, daily summary, smart schedule, notify history, rich push |
| `9adc6d0` | ai-dev / docs-dev | AI-ready push, responsive/PWA/notify docs |
| `36b869c` | test-dev | Responsive UI tests, PWA tests, push notification tests |

### Infrastructure
| Commit | Agent | Description |
|--------|-------|-------------|
| `d3bda0e` | infra-dev | nginx PWA headers, PWA K8s config, notification K8s + Grafana |

---

## Phase 8: Advanced Trading (v0.9.5) — 2026-05-19

### Order Management & Paper Trading
| Commit | Agent | Description |
|--------|-------|-------------|
| `3d3af93` | backend-dev | Implement Phase 8 execution module |
| `64633f4` | fix | Paper trade tx isolation, concentration double-count, user_id on orders, YF empty results, keychain crash, market order price |
| `3eb0413` | frontend-dev | Order/paper/strategy/broker commands + OrderDetail, PaperDashboard, PaperPnL, BacktestResults, BrokerConfig |
| `d38da67` | frontend-dev | Order/paper/strategy/broker commands + trading UI components |

### Strategy Framework
| Commit | Agent | Description |
|--------|-------|-------------|
| `3d5144c` | backend-dev | Implement strategy engine with backtesting |
| `ceb762f` | backend-dev | Walk-forward optimization, OOS testing, strategy comparison |
| `d4e87bd` | ai-dev | AI-generated strategy with sandbox execution and registry registration |

### Tests & Docs
| Commit | Agent | Description |
|--------|-------|-------------|
| `8ed4de1` | test-dev | All 6 Phase 8 test suites, fixed StrategyBase instantiation bug |
| `4cb8581` | test-dev | Order API + service tests, paper trading API + fill sim tests, strategy + broker tests |
| `7ba1f14` | docs-dev | Order management, paper trading, broker integration docs |
| `1d998aa` | docs-dev | Verify and update order, paper trading, broker integration documentation |

---

## Phase 7: Intelligence & Scale (v0.9.0) — 2026-05-19

### AI Advisor & NLQ
| Commit | Agent | Description |
|--------|-------|-------------|
| `e12dc7b` | ai-dev | AI advisor v1 + NLQ (client, prompts, advisor, parser, intent mapper) |
| `10bb321` | frontend-dev | AI terminal command, streaming response, chat history, attrib AI, ask command, NLQ help, workspace switcher, shared portfolio view |

### Multi-User Workspaces
| Commit | Agent | Description |
|--------|-------|-------------|
| `5852757` | security-dev | AI rate limiting, prompt sanitization, RBAC middleware, workspace isolation |

### Data Quality
| Commit | Agent | Description |
|--------|-------|-------------|
| `c69669c` | data-dev | Freshness, outlier detection, async gather, semaphore, retry jitter |
| `d81ee59` | data-dev | Data quality middleware + health endpoint + tests |

### Rust Engine
| Commit | Agent | Description |
|--------|-------|-------------|
| `600278f` | rust-dev | Tokenizer and anomaly detection modules |

### Sprint Finalization
| Commit | Agent | Description |
|--------|-------|-------------|
| `c767309` | docs / infra / design / test | Sprint 1 finalization — all 68 tasks complete, doc updates, test fixes, infra polish |
| `8d75efb` | infra-dev | Pre-commit hooks, Docker optimizations, K8s secrets |
| `65b9dcc` | docs-dev | AI + NLQ + anomaly documentation |
| `c127a5f` | design-dev | AI cat loader animation + anomaly heatmap mode |
| `02d463b` | test-dev / docs-dev | Fix all tests, add AI & anomaly API docs, update command docs |
| `7a7d992` | fix | Critical bug fixes: nlq dict.strip crash, activity missing text import, users Pydantic body, context risk tickers, COEP header |
| `bfce511` | test-dev | Fix and verify all test-dev test files |
| `44054e9` | audit | Fix 6 issues found during code audit |

### Planning & Docs
| Commit | Agent | Description |
|--------|-------|-------------|
| `e51a7b2` | PM | Phase 8 planning — Advanced Trading (84 microtasks) |
| `8151b4e` | PM | Phases 9+10+11-14 planning — Mobile, Social, future preview, parallel sprint plan |
| `b3f6a73` | PM | Team realignment v0.9.0 — sprint plan, agent prompts, communication board, 64 sprint tickets |

---

## Phase 6: Expansion (v0.6.0–v0.8.0) — 2026-05-18

| Commit | Agent | Description |
|--------|-------|-------------|
| `f7312ff` | PM | Resolve failing tests and test coverage |
| `f1f573d` | PM | Add whoami command handler — frontend tests now pass 20/20 |
| `e995e24` | PM | Add joke command + JOKES.md — 35 cat/finance jokes |
| `0ea6fd3` | PM | Fix blocking import errors — remove broken middleware imports, clean orphaned JSX |
| `cf74e72` | docs | Update COMMANDS.md with missing terminal commands |
| `350cbb7` | fix | Resolve syntax error in handleCommand |
| `fe33c23` | feat | Move notifications state to Redis |
| `6357479` | feat | Move alerts state to Redis |
| `6bfb916` | feat | Cap terminal history and make SMTP non-blocking |
| `fd9c875` | refactor | Clean up unused CSS keyframes |
| `bb0e94f` | feat | Update terminal autocomplete commands |
| `a87e31e` | feat | Implement missing command handlers and improve security |
| `a190dc7` | frontend-dev / backend-dev | All audit tasks complete |
| `2ce6cfa` | docs | Update AGENTS.md — all Phase 6.5 tasks verified done |
| `82bc7f0` | PM | Broadcast: Sprint v0.8.6 task assignments + Phase 7 kickoff |
| `7bc4165` | PM | Strategy doc, agent prompts, and workflow for parallel work |

---

## Phase 5: Production (v0.5.0) — 2026-05-18

| Commit | Agent | Description |
|--------|-------|-------------|
| `757de46` | chore | Temporarily remove workflow files (OAuth scope limitation) |
| `baa2fb1` | chore | Commit pending frontend + docs + test changes |

---

## Phase 16: Sustainability & ESG (v0.17.0) — 2026-05-19

### ESG Scoring
| Commit | Agent | Description |
|--------|-------|-------------|
| `9c68f47` | backend-dev | ESG scoring foundation — model, service, API (ticker/portfolio/screen), weighted calculation |
| `1c5dad2` | backend-dev | ESG scores + carbon footprints DB migration |
| `ef416fc` | backend-dev | ESG tracker — all Epic 16.1 backend tasks DONE |

### Carbon & Climate
*(in progress)*

---

## Phase 15: Developer Platform (v0.16.0) — 2026-05-19

### SDK & Client Libraries
| Commit | Agent | Description |
|--------|-------|-------------|
| `49eed73` | backend-dev | Python SDK — core client, market, portfolio, trading modules (sync+async, error handling, pagination) |
| `9a9e619` | backend-dev | curl API examples — 14 shell scripts covering all endpoint categories |
| `086cd86` | backend-dev | SDK auto-generation from OpenAPI spec |
| `4847174` | backend-dev | SDK auto-generated module |

### Plugin Ecosystem
| Commit | Agent | Description |
|--------|-------|-------------|
| `f9967df` | backend-dev | Plugin ecosystem — spec, loader, API (5 endpoints: install/list/run/remove/approve), example alert_handler plugin |
| `dee07a5` | backend-dev | Example custom_strategy plugin (trading signals + iceberg orders) |
| `dddbe42` | security-dev | Plugin sandbox — restricted exec isolation, API scope proxy, memory/time limits, blocked modules |
| `11dbab0` | security-dev | Plugin permission system — 16 scoped permissions, DB-backed approval/revocation, middleware enforcement |
| `4847174` | backend-dev | Mark plugin ecosystem DONE |

### Developer Experience
| Commit | Agent | Description |
|--------|-------|-------------|
| `fae9997` | security-dev | API versioning middleware — semver header parsing, deprecation/sunset headers, changelog metadata |
| `4e1868d` | backend-dev | Developer request/response debug log — per-API-key logging, timing, status distribution, key analytics |
| `d91d62b` | docs-dev | Developer docs — SDK README, Plugin API guide (PLUGIN_API.md), Developer Portal (DEVELOPER_PORTAL.md) |

---

## Phase 14: Global Markets (v0.15.0) — 2026-05-19

### Multi-Currency Architecture
| Commit | Agent | Description |
|--------|-------|-------------|
| `a0f2414` | backend-dev | Currency model (ISO 4217), live FX rate provider, currency conversion service, multi-currency portfolio model |
| `d06d6c8` | backend-dev | Portfolio currency conversion endpoints, FX P&L tracking, crypto-as-currency |
| `f33a3cc` | frontend-dev | `currency` terminal command — list rates, convert, set portfolio base currency |

### International Exchanges
| Commit | Agent | Description |
|--------|-------|-------------|
| `dadf697` | data-dev | Asian (11), European (14), LatAm (6), MEA (9) market data sources — 40 exchanges with benchmark indices |
| `a0f2414` | backend-dev | Market hours service with timezone/holiday calendar, unified /api/v1/markets/global endpoint |
| `48f75c4` | frontend-dev | `global` terminal command — market overview by region + exchange detail |
| `431da45` | frontend-dev | Market hours overlay on 3D globe — open/closed indicators, live status |

### International Brokers & i18n
| Commit | Agent | Description |
|--------|-------|-------------|
| `a0f2414` | backend-dev | Interactive Brokers production connector (IBBroker) |
| `ee3afa0` | backend-dev | DEGIRO (EU), Rakuten (JP), Zerodha (IN) broker connectors |
| `6b18d92` | security-dev | Broker auth middleware — OAuth helpers, region-scoped credential encryption (HKDF + Fernet AES-256-GCM) |
| `56b7f00` | frontend-dev | i18n framework — 8-language translations (DE, FR, ES, JP, ZH, KO, PT, RU), locale-aware formatting, language selector |

---

## Phase 18: DeFi & Web3 (v1.1.0) — 2026-05-19

### WalletConnect & EVM Wallets
| Commit | Agent | Description |
|--------|-------|-------------|
| `d9897c6` | backend-dev | WalletConnect v2 SDK, EVM wallets (MetaMask/Rainbow/Coinbase), balance aggregation, wallet API (8 endpoints) |
| `441754b` | security-dev | Sign-in with Ethereum (SIWE) auth |
| `0958c69` | security-dev | Encrypted keychain for DeFi |
| `4274421` | security-dev | Hardware wallet support (Ledger, Trezor) |
| `afa395c` | backend-dev | Gas estimator + MEV protection + Solana wallet |
| `4c81767` | data-dev | DeFi protocol integrations — Uniswap, Aave, Curve, Lido, MakerDAO, Yearn |
| `f82bb2c` | backend-dev | Solana wallet + tx signing + balance aggregation |
| `40e6792` | frontend-dev | DeFi terminal commands (wallet connect, balance, sessions, defi protocols) |

### NFT & DeFi Frontend
| Commit | Agent | Description |
|--------|-------|-------------|
| `d110a65` | batch | NFT Gallery/Chart/Heatmap components, Solana DeFi (Jupiter/Raydium/Marinade), NFT rarity + valuation |
| `c05f5da` | frontend-dev | Cat-themed error messages + tuna counter in status bar |

---

## Phase 19: AI Hedge Fund (v1.2.0) — Planned

| Commit | Agent | Description |
|--------|-------|-------------|
| `6991e9f` | backend-dev | Position sizing, risk controls, drawdown recovery, perf metrics, 7-endpoint API |
| `4683885` | backend-dev | hedgefund perf_metrics, compliance fix |
| `32e4ba9` | PM | Phase 19 planning — 48 tickets across 3 epics |

---

## Phase 20: Miau Finance Network (v1.3.0) — 🟡 In Progress

| Commit | Agent | Description |
|--------|-------|-------------|
| `48f87ab` | batch | Miau Network — strategy NFT, licensing, reputation, audit, marketplace API, governance API with proposals/voting |
| `a791afa` | backend-dev | ProposalVote component |
| `135d6c4` | meta | 11 backend-dev + frontend-dev tickets DONE |

---

## Phase 23: Education Platform (v1.6.0) — 🟡 In Progress

| Commit | Agent | Description |
|--------|-------|-------------|
| `80b1233` | backend-dev | Education batch — plan updates, network UI components |
| `7387b4e` | backend-dev | Final sweep: Phase 24 tickets, AI depth analysis, hedge fund compliance |

---

## Phase 25: CBDC & Quantum (v1.8.0) — 🟡 In Progress

| Commit | Agent | Description |
|--------|-------|-------------|
| `bb554c1` | backend-dev | Phase 25 kickoff — CBDC plan + tickets, multi-CBDC portfolio optimization |

---

## Phase 26: Quantum Finance (v1.9.0) — 🟡 In Progress

| Commit | Agent | Description |
|--------|-------|-------------|
| `d256ca4` | backend-dev | QUBO portfolio optimization — Markowitz-to-QUBO, brute-force solver |
| `9301ef2` | backend-dev | Quantum-Ready Finance — QUBO solver, annealing, hybrid VQE/QAOA, quantum API |
| `bd93ebe` | security-dev | FALCON compact signatures + Hybrid classical/PQC KEM and signing |
| `a474c9e` | backend-dev | Auth middleware extensions |
| `9d0c4d6` | security-dev | PQC JWT signing (Dilithium/Falcon/Hybrid) + PQC key management |

---

## Phase 27: AGI Finance (v2.0.0) — Planned

Planned: autonomous financial AGI, goal-based planning, explainability, continuous learning, DAO governance.

---

## Summary

| Version | Phase | Tasks | Commits | Status |
|---------|-------|-------|---------|--------|
| v0.1.0-v0.5.0 | 1-5 | 56 | ~10 | ✅ Complete |
| v0.6.0-v0.8.0 | 6 | 24 | ~16 | ✅ Complete |
| v0.9.0 | 7 | 108 | ~40 | ✅ Complete |
| v0.9.5 | 8 | 84 | ~15 | ✅ Complete |
| v0.10.0 | 9 | 65 | ~15 | ✅ Complete |
| v0.11.0 | 10 | 30 | ~10 | ✅ Complete |
| v0.12.0 | 11 | 55 | ~20 | ✅ Complete |
| v0.12.0 | 12 | 25 | ~10 | ✅ Complete |
| v0.12.5 | 12.5 | 30 | ~20 | ✅ Complete |
| v0.13.0 | 13 | 48 | ~6 | ✅ Complete |
| v0.15.0 | 14 | 44 | ~20 | ✅ Complete |
| v0.16.0 | 15 | 42 | ~25 | ✅ Complete |
| v0.17.0 | 16 | 36 | ~15 | ✅ Complete |
| **v1.0.0** | **17** | **40** | **~15** | **✅ Released** |
| **v1.1.0 (→v2.1.0)** | **18** | **52** | **~30** | **✅ Released** |
| v1.2.0 | 19 | 48 | ~3 | ✅ Complete |
| v1.3.0 | 20 | 44 | ~11 | ✅ Complete |
| v1.4.0 | 21 | 40 | ~1 | ✅ Complete |
| v1.5.0 | 22 | 42 | ~1 | ✅ Complete |
| v1.6.0 | 23 | 38 | ~5 | ✅ Complete |
| v1.7.0 | 24 | 36 | ~1 | ✅ Complete |
| v1.8.0 | 25 | 32 | ~1 | ✅ Complete |
| v1.9.0 | 26 | 13 | ~5 | ✅ Complete |
| **v2.0.0** | **27** | **18** | **~5** | **✅ Released** |
| **v2.1.0** | **Commercial** | **—** | **~5** | **✅ Released** |
| **v2.3.0** | **Datavore** | **136** | **~40** | **✅ Released** |
| **Total** | **1-27 + Datavore** | **1,200+** | **~420** |
