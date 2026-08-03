# Miau Finance — Production Deployment Guide

> **Commercial Release v2.1.0 "Pawborghini Edition"**
> Proprietary software — All Rights Reserved.
> Deploy on your infrastructure after purchasing a license.

---

## Quick Start (5 minutes)

> ⚠️ **License Required:** This is proprietary software. A valid license key is required for production use.
> Contact sales@miau.finance for licensing.

```bash
curl -fsSL https://raw.githubusercontent.com/LuZziD/cat-finance-analytics-shell-miau/main/scripts/install.sh | bash
```

This will:
1. Check dependencies (Docker, Git)
2. Request your license key
3. Clone the repository
4. Generate secure secrets (JWT, DB passwords, API keys)
5. Start all 10 Docker services
6. Print the login URL and credentials

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Disk | 20 GB free | 50 GB SSD |
| Docker | 24.0+ | 25.0+ |
| Docker Compose | v2.20+ | v2.25+ |
| OS | Linux (any) | Ubuntu 22.04 / Debian 12 |

---

## Manual Installation

### 1. Clone the Repository

```bash
git clone --depth 1 --branch main https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd cat-finance-analytics-shell-miau
```

### 2. Configure Environment

```bash
cp .env.example .env
```

**Required environment variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_SECRET_KEY` | JWT signing key (32+ chars) | Auto-generated |
| `POSTGRES_PASSWORD` | Database password | Auto-generated |
| `DATABASE_URL` | Async PostgreSQL connection | auto |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:5173` |

### 3. Start Services

```bash
# Development mode
docker compose up -d

# Production mode (3× backend replicas, PgBouncer, nginx frontend)
docker compose -f docker-compose.prod.yml up -d

# Auto-setup: generate all passwords + prompt for API keys
bash scripts/install-miau.sh

# Validate existing .env
bash scripts/install-miau.sh --validate
```

### 4. Verify

```bash
curl http://localhost:8000/api/v1/health
# {"status":"ok","app":"Miau Finance"}
```

### 5. Login

Open `http://localhost:5173` and login with your credentials

---

## Services

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 5173 | Terminal UI |
| Backend | 8000 | REST API + WebSocket |
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Cache + rate limiting |
| MinIO | 9000 | S3-compatible storage |
| Cube.js | 4000 | Analytics API |
| Superset | 8088 | BI dashboards |
| Airflow | 8080 | Scheduled jobs |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Visualization |

---

## Backup & Restore

### Database

```bash
# Backup
docker exec miau-finance-postgres-1 pg_dump -U miau miau > backup.sql

# Restore
cat backup.sql | docker exec -i miau-finance-postgres-1 psql -U miau miau
```

### Configuration

Back up `.env` and `docker-compose*.yml` files — they contain your secrets and setup.

---

## Upgrading

```bash
cd /path/to/miau-finance
git pull
docker compose pull
docker compose up -d
docker exec miau-finance-backend-1 alembic upgrade head
```

---

## Monitoring

- **Grafana**: `http://localhost:3000` (admin / GRAFANA_PASSWORD)
- **Prometheus**: `http://localhost:9090`
- **Service logs**: `docker compose logs -f backend`

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Check `docker compose logs backend` for errors |
| Database connection failed | Verify `POSTGRES_PASSWORD` matches in .env |
| Port already in use | Change the host port in `docker-compose.yml` |
| Can't login | Check credentials and backend logs |
| AI not working | Set `AI_API_KEY` in .env |
| Trading not working | Set `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` in .env |

---

## V6 MiauGeology Ecosystem (Standalone Vite Services)

The V6 Purrantir MiauGlobe update adds 8 standalone Vite frontend services alongside the Docker stack.

| Port | Service | Command |
|------|---------|---------|
| 5173 | Terminal UI | `cd miau-finance/frontend && npx vite --host --port 5173` |
| 5174 | Education Platform | `cd miau-finance/education-platform && npx vite --host --port 5174` |
| 5175 | Ecosystem Site | `cd miau-finance/ecosystem-site && npx vite --host --port 5175` |
| 5176 | Marketing Dashboard | `cd miau-finance/marketing-dashboard && npx vite --host --port 5176` |
| 5177 | Log Viewer | `cd miau-logviewer && npx vite --host --port 5177` |
| 5178 | MiauBook | `cd miau-book && npx vite --host --port 5178` |
| 5179 | Miau Admin | `cd miau-admin && npx vite --host --port 5179` |
| 5181 | Cat Galaxy | `cd cat-galaxy && npx vite --host --port 5181` |

### Immortal Cat Service Manager

All 8 Vite services are managed by a systemd user service for auto-restart:

```bash
# Status
systemctl --user status immortal-cat.service

# Restart all Vite services
systemctl --user restart immortal-cat.service

# Follow logs
journalctl --user -u immortal-cat.service -f

# Configuration
# File: /home/jevgeniz/Projekte/immortal-cat.sh
```

The immortal-cat script checks ports every 15 seconds (`RestartSec=15` in systemd). If a Vite service crashes, it's automatically restarted. The script uses `fuser` to detect real processes (not ghost sockets).

### Ordering

Start the Docker stack first (backend, postgres, redis), then the Vite services:

```bash
# 1. Docker stack
cd miau-finance && docker compose up -d

# 2. Start immortal-cat (if not already running)
systemctl --user start immortal-cat.service

# 3. Verify all 8 ports respond
for p in 5173 5174 5175 5176 5177 5178 5179 5181; do
  curl -s -o /dev/null -w "Port $p: %{http_code}\n" http://localhost:$p
done
```

The Docker backend (port 8000) and standalone frontends (ports 5173-5181) are independent — you can run the terminal without the ecosystem services, and vice versa.
