# Miau Finance — Service Map & Port Reference

## Running Services

| Port | Service | Type | Status | Purpose | Can Disable? |
|------|---------|------|--------|---------|-------------|
| 3000 | Grafana | Docker | ✅ | Dashboards, alerts, metrics visualization | Optional |
| 3001 | Homepage | Standalone | ✅ | Marketing site (Next.js, v2.3.0 Datavore) | Optional |
| 5173 | Frontend | Standalone | ✅ | Main terminal UI (Vite + React) | 🔴 Required |
| 5174 | Education | Standalone | ✅ | Learning platform (230 courses, 18 certs) | Optional |
| 5175 | Ecosystem | Standalone | ✅ | Corp landing page (Miau Corp) | Optional |
| 5176 | Marketing Dashboard | Standalone | ✅ | Miau marketing analytics | Optional |
| 5177 | Log Viewer | Standalone | ✅ | Real-time log stream | Optional |
| 5178 | MiauBook | Standalone | ✅ | Cat social network for traders | Optional |
| 5179 | Miau Admin | Standalone | ✅ | Admin console (user/team mgmt) | Optional |
| 5181 | Cat Galaxy | Standalone | ✅ | Service health dashboard with orbiting planets | Optional |
| 5433 | PostgreSQL | Docker | ✅ | Primary database | 🔴 Required |
| 6379 | Redis | Docker | ✅ | Cache + rate limiting | 🔴 Required |
| 8000 | Backend API | Docker | ✅ | FastAPI — 515+ endpoints, 50+ data providers | 🔴 Required |
| 8088 | Apache Superset | Docker | ✅ | SQL-native BI platform | Optional |
| 9000-9001 | MinIO | Docker | ✅ | S3-compatible object storage | Optional |
| 9090 | Prometheus | Docker | ✅ | Metrics collection | Optional |

## Freed Ports (Standalone Duplicates Eliminated)

These features are still accessible through the main application — the standalone servers were redundant.

| Port | Service | Alternative Access |
|------|---------|-------------------|
| ~~5176~~ | Marketing Dashboard | Data available via Grafana dashboards or backend APIs |
| ~~5177~~ | Log Viewer | **http://localhost:8000/logs-viewer/** (served by backend) |
| ~~5178~~ | MiauBook | Type `miaubook` in the terminal |
| ~~5179~~ | Admin Console | Type `admin` in the terminal |

## Quick Start

### Start Everything

```bash
# Core containers (required)
cd miau-finance && docker compose up -d                 # Backend + DB + Redis
cd miau-homepage && npx next dev -p 3001 &               # Marketing site
cd miau-finance/frontend && npx vite --host 0.0.0.0 &    # Terminal UI
cd cat-galaxy && npx vite --host 0.0.0.0 --port 5181 &   # Service dashboard
```

### Verify It's Working

```bash
curl http://localhost:8000/api/v1/health         # Backend
curl http://localhost:5173/                       # Terminal UI
curl http://localhost:3001/                       # Homepage
curl http://localhost:5181/                       # Cat Galaxy
```

## Service Dependencies

```
Frontend (5173) ──→ Backend API (8000) ──→ PostgreSQL (5433)
                                        ──→ Redis (6379)
                                        ──→ MinIO (9000)
                                        ──→ 50+ external data providers
```

All other services are independent and can be stopped/started without affecting the core trading platform. Only the Backend API, PostgreSQL, and Redis are required for full functionality.

## Persistence

All Vite ports (5173-5181) are managed by the **Immortal Cat** systemd service:

```bash
systemctl --user status immortal-cat.service    # Check status
systemctl --user restart immortal-cat.service   # Restart all Vite services
journalctl --user -u immortal-cat.service -f    # Follow the cat's log
```

The script at `/home/jevgeniz/Projekte/immortal-cat.sh` auto-restarts services every 15 seconds if they crash. It manages exactly these services: 5173 (frontend), 5174 (education), 5175 (ecosystem), 5176 (marketing), 5177 (logviewer), 5178 (miau-book), 5179 (miau-admin), 5181 (cat-galaxy).
