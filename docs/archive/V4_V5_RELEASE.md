# 🐱 V4 "The Great Fixing Era" + V5 "Purring Production"

> **Current version:** v2.3.0 (Datavore Edition) + V4 Delittering + V5 Hardening
> **Tests:** 729+ passing · **Services:** 10 Docker + 7 standalone host services

---

## V4 — The Great Fixing Era (Delittering the Litterbox)

Debt cleanup, dead code removal, and codebase tightening after the Datavore data explosion.

### V4-001: Remove Dead Bloat

| Task | What | Files |
|------|------|-------|
| V4-001a | Removed duplicate **11.5MB companies.json** (WorldMap and MiauGlobe now lazy-fetch from continent-sharded API) | `frontend/src/data/companies.json` |
| V4-001b | Removed `.venv/` and `venv/` from git tracking + gitignore | `.gitignore`, `.venv/`, `backend/venv/` |
| V4-001c | Flattened nested `logviewer/logviewer/` directory | `backend/app/static/logviewer/` |
| V4-001d | Removed old `companies.json` from `frontend/public/data/` (replaced by 7 continent shards) | `frontend/public/data/companies.json` |

**Impact:** Repo size reduced by ~22MB, bundle size dropped from 2.2MB to manageable levels.

### V4-002: Consolidate Map Effects

| Task | What | Files |
|------|------|-------|
| V4-002a | Merged tile layer + weather overlay into one useEffect | `WorldMap.tsx` |
| V4-002b | Merged resize observer into init effect | `WorldMap.tsx` |
| V4-002c | Removed empty mount effect | `WorldMap.tsx` |
| V4-002d | Removed duplicate tile layer effect (was causing race condition on zoom) | `WorldMap.tsx` |

**Impact:** WorldMap useEffect count reduced from 12 to 8, eliminating zoom weather flicker.

### V4-003: Fix All Warnings

| Task | What | Files |
|------|------|-------|
| V4-003a | Fixed `billing_balances` migration — created missing table | `alembic/versions/` |
| V4-003b | Fixed SecuritiesDB no-screener error in screener endpoint | `backend/app/api/datavore.py` |
| V4-003c | Fixed Yahoo provider bare `DataSourceError` (added try/except wrapper) | `backend/app/services/data/providers/yahoo.py` |
| V4-003d | Fixed stale version references in education platform | `education-platform/src/` |

### V4-004: Optimize Bundle

| Task | What | Result |
|------|------|--------|
| V4-004a | Removed unused imports from WorldMap.tsx | No unused imports found ✅ |
| V4-004c | Tree-shook unused Leaflet controls | All controls in use ✅ |
| V4-005b | Verify `make up` starts all 9 containers cleanly | 9/9 containers healthy ✅ |

### Infrastructure Changes

| Change | Details |
|--------|---------|
| Port 5177 | Freed from Docker → dedicated to standalone Log Viewer |
| Port 5178 | Freed from Docker → dedicated to MiauBook |
| Port 5179 | Freed from Docker → dedicated to Admin panel |
| `.env.example` | Added entries for 8 missing API keys |
| `SERVICES.md` | Created port map + quick-start reference |

---

## V5 — Purring Production (Stable, Fast, Everywhere)

Production-hardening sprint: monitoring, mobile, terminal UX, and infrastructure reliability.

### S-001: Health & Monitoring

| ID | Task | What | Files |
|----|------|------|-------|
| S-001a | Slack/Discord webhook alerts | Fires when providers go unhealthy, uses `SLACK_WEBHOOK_URL`, rate-limited to 1/5min via Redis | `backend/app/api/health.py` |
| S-001b | `health` terminal command | Shows uptime, provider statuses, log file sizes | `frontend/src/lib/commands.ts` |
| S-001c | Cat Galaxy health endpoint | `GET /api/v1/health/services` — checks all 10 Miau services in parallel | `backend/app/api/health.py`, `cat-galaxy/src/App.tsx` |
| S-001d | Redis health history | Health results stored in Redis (7d TTL), queryable via `GET /api/v1/health/history?hours=N` | `backend/app/api/health.py` |

**New endpoints:**
- `GET /api/v1/health` — provider health + log status + uptime
- `GET /api/v1/health/services` — all service health (Docker + host)
- `GET /api/v1/health/history?hours=24` — historical health data

### S-002: Mobile & PWA

| ID | Task | What | Files |
|----|------|------|-------|
| S-002a | PWA service worker v3 | Offline fallback page (`/offline.html`), command API caching, push event listener with notification actions | `frontend/public/sw.js` |
| S-002b | Touch gestures | Swipe down → command palette, swipe left/right → cycle views (heatmap↔benchmark↔correlation) | `Terminal.tsx` |
| S-002c | Responsive layout | 640px + 380px breakpoints: smaller fonts, tighter padding, stacked status bar | `Terminal.tsx` |
| S-002d | Push notifications | `POST /push/send` and `POST /push/broadcast` endpoints, VAPID JWT auth in `send_web_push()`, notification click handling | `backend/app/api/push_notifications.py`, `backend/app/services/web_push.py` |

### S-003: Grafana Dashboards

| ID | Dashboard | Panels | File |
|----|-----------|--------|------|
| S-003a | Provider Health | Health overview stat, unhealthy count, uptime gauge, health over time, total requests, error rate, avg response time | `grafana/dashboards/provider-health.json` |
| S-003b | API Endpoint Usage | Request/error rate graphs, top 10 endpoints table, top 10 error endpoints, error %, request duration | `grafana/dashboards/api-usage-detailed.json` |
| S-003c | User Activity | Active users, total requests, error count, health %, activity/error/provider graphs, hourly heatmap | `grafana/dashboards/user-activity.json` |

**New Prometheus metrics:** `miau_providers_healthy`, `miau_providers_unhealthy` added to `/metrics` endpoint for dashboard consumption.

### S-004: Terminal UX

| ID | Task | What | Files |
|----|------|------|-------|
| S-004a | Persistent history | Command history saved to `localStorage` across sessions (last 500 commands) | `Terminal.tsx` |
| S-004b | Better autocomplete | Added 57 missing commands to `COMMAND_META` (achievements, catberg, defi, global, health, screener, etc.) with descriptions, args, and subcommands | `autocomplete.ts` |
| S-004c | Tuna counter | 🐟 displayed in status bar showing `cmdCount / 3` tuna earned | `Terminal.tsx` |
| S-004d | `cat --pet` animation | Purring ASCII cat with tuna, paw prints, and sound effects | `Terminal.tsx` |

### S-005: Infrastructure

| ID | Task | What | Files |
|----|------|------|-------|
| S-005a | Docker healthchecks | Added healthchecks to frontend, superset, airflow, education-platform — all 10 services now have health checks | `docker-compose.yml` |
| S-005b | auto-restart script | `scripts/start.sh` now uses `fuser -k` for thorough port cleanup, kills all governour variants | `scripts/start.sh` |
| S-005c | .env validation | Startup checks for Stripe keys, Slack webhook, SMTP, demo API keys; warns in production | `backend/app/config.py` |
| S-005d | Redis pool tuning | Shared connection pool (`max_connections=10`, `socket_keepalive`, `health_check_interval=30`) between rate limiter and cache module | `rate_limit.py`, `cache.py` |

### S-006: Testing

| ID | Tests | File |
|----|-------|------|
| S-006a | 9 health endpoint tests (structure, services, history, metrics, timestamps, version) | `backend/tests/test_api/test_health.py` |
| S-006b | 11 fallback tests (+4 new: timeout, rate limit, multi-capability, empty registry) | `backend/tests/test_data/test_fallback.py` |
| S-006c | 8 Cat Galaxy screen tests (render, health fetch, icons, hover tooltip, legend) | `frontend/tests/catgalaxy.test.tsx` |

### Pentest Fixes

| Issue | Finding | Fix |
|-------|---------|-----|
| LOW-002 | FRED API silently used `"demo"` fallback key | Now raises HTTP 400 when key is `"demo"` or missing |
| INFO-001 | Missing HSTS header | Already handled by existing `SecurityHeadersMiddleware` |
| INFO-002 | `/metrics` public | Intentional — Prometheus scraping requires open access |

---

## Port Map

| Port | Service | Method |
|------|---------|--------|
| 5173 | Terminal frontend | Vite standalone |
| 5174 | Education portal | Vite standalone |
| 5175 | Miau Corp | Python HTTP server |
| 5176 | Marketing dashboard | Vite standalone |
| 5177 | Log Viewer | Vite standalone |
| 5178 | MiauBook | Vite standalone |
| 5179 | Admin panel | Vite standalone |
| 5181 | Cat Galaxy | Vite standalone |
| 3000 | Grafana | Docker |
| 3001 | Homepage (Next.js) | Standalone |
| 8000 | Backend API | Standalone uvicorn |
| 8080 | Airflow | Docker |
| 8088 | Superset | Docker |
| 9090 | Prometheus | Docker |

---

## Key Files Changed (V4+V5)

| File | Change |
|------|--------|
| `backend/app/api/health.py` | Webhook alerts, services endpoint, health history, provider metrics |
| `backend/app/api/push_notifications.py` | Send + broadcast push endpoints |
| `backend/app/api/analytics/fred.py` | Demo key → HTTP 400 |
| `backend/app/services/web_push.py` | VAPID JWT auth for web push |
| `backend/app/config.py` | .env validation, slack_webhook_url, Stripe/SMTP warnings |
| `backend/app/cache.py` | Redis connection pooling |
| `backend/app/middleware/rate_limit.py` | Shared Redis pool, tuned connection settings |
| `backend/app/middleware/metrics.py` | Provider health metrics |
| `frontend/public/sw.js` | Offline page, push events, command caching |
| `frontend/src/components/Terminal.tsx` | Touch gestures, responsive layout, cat --pet, history |
| `frontend/src/lib/autocomplete.ts` | 57 missing commands added |
| `cat-galaxy/src/App.tsx` | Centralized health endpoint |
| `docker-compose.yml` | Healthchecks for all 10 services |
| `scripts/start.sh` | fuser -k cleanup, governour kill |
| `grafana/dashboards/*.json` | 3 new provisioning dashboards |
| `backend/tests/test_api/test_health.py` | 9 new health tests |
| `backend/tests/test_data/test_fallback.py` | 4 new fallback tests |
| `frontend/tests/catgalaxy.test.tsx` | 8 new Cat Galaxy tests |
