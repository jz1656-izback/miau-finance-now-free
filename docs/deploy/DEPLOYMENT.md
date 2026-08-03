# MIAU FINANCE — Deployment Guide

```
   ╱|、
  (˚ˎ 。7     "From localhost to production. The cat does not tolerate downtime."
   |、˜〵      "Follow these steps exactly. The cat is watching."
   じしˍ,)ノ    "If something breaks, you broke it. Fix it."
```

## Architecture Overview

```
User → DNS (miau.finance) → Cloudflare/CDN → Docker Host
                                                   │
                        ┌──────────────────────────┴──────────────────────────┐
                        │                    Docker Host                       │
                        │  ┌─────────┐ ┌────────┐ ┌──────────┐ ┌───────────┐ │
                        │  │ Backend │ │Frontend│ │ Postgres │ │   Redis   │ │
                        │  │ :8000   │ │ :5173  │ │ :5432    │ │ :6379     │ │
                        │  └─────────┘ └────────┘ └──────────┘ └───────────┘ │
                        │  ┌─────────┐ ┌────────┐ ┌──────────┐ ┌───────────┐ │
                        │  │ MinIO   │ │ Cube   │ │ Grafana  │ │Prometheus  │ │
                        │  │ :9000   │ │ :4000  │ │ :3000    │ │ :9090     │ │
                        │  └─────────┘ └────────┘ └──────────┘ └───────────┘ │
                        └────────────────────────────────────────────────────┘
```

## Prerequisites

- Docker 24+ with Compose V2
- 4 GB RAM minimum (8 GB recommended for full profile)
- Domain with DNS pointing to your host
- SMTP server for transactional emails (Stripe receipts, password reset)

## Quick Start (Development)

```bash
# Light profile (~200 MB RAM, 4 services)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Full profile (~5 GB RAM, 12 services)
docker compose up -d

# Check health
curl http://localhost:8000/api/v1/health
curl http://localhost:5173
```

## Production Deployment

### 1. DNS Setup

| Record | Type | Value |
|--------|------|-------|
| `miau.finance` | A | `<your-server-ip>` |
| `api.miau.finance` | A | `<your-server-ip>` |
| `app.miau.finance` | CNAME | `miau.finance` |

### 2. SSL Certificates

```bash
# Install certbot, get wildcard cert
certbot certonly --manual --preferred-challenges dns -d "*.miau.finance" -d miau.finance
# Certs land in /etc/letsencrypt/live/miau.finance/
```

### 3. Environment Setup

```bash
cp .env.example .env
# Edit .env with production values:
#   ENVIRONMENT=production
#   POSTGRES_PASSWORD=<random-40-chars>
#   REDIS_PASSWORD=<random-40-chars>
#   SECRET_KEY=<random-32-chars>
#   JWT_SECRET_KEY=<random-32-chars>
#   STRIPE_SECRET_KEY=pk_live_...
#   STRIPE_WEBHOOK_SECRET=whsec_...
```

### 4. Database

```bash
# Production: use managed PostgreSQL (AWS RDS, Railway, etc.)
# Update DATABASE_URL in .env accordingly

# Or self-hosted with persistent volume:
docker compose up -d postgres
docker compose exec postgres psql -U miau -d miau -f services/postgres/init/*.sql
```

### 5. Launch Stack

```bash
docker compose up -d --build
```

### 6. Verify

```bash
# Health check
curl https://api.miau.finance/api/v1/health

# Frontend
curl https://app.miau.finance

# Login with demo credentials
curl -X POST https://api.miau.finance/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<demo-password-from-env>"}'
```

## Deployment Profiles

| Profile | Services | RAM | Use Case |
|---------|----------|-----|----------|
| **Light** (dev) | backend, frontend, postgres, redis | ~200 MB | Development, testing |
| **Standard** | All 12 services | ~5 GB | Production with monitoring |
| **Kubernetes** | All services, auto-scaling | Variable | Production at scale |

## Scaling

```bash
# Increase backend workers
docker compose up -d --scale backend=3

# Kubernetes auto-scaling (existing HPA)
kubectl apply -f k8s/hpa.yaml
```

## Backup & Restore

```bash
# PostgreSQL
docker compose exec postgres pg_dump -U miau miau > backup_$(date +%Y%m%d).sql
docker compose exec -T postgres psql -U miau miau < backup.sql

# MinIO data
docker compose exec minio mc mirror --overwrite /data /backup/minio

# Redis
docker compose exec redis redis-cli SAVE
docker cp miau-redis-1:/data/dump.rdb ./redis-backup.rdb
```

## Monitoring

| Tool | URL | Purpose |
|------|-----|---------|
| Grafana | `http://host:3000` | Dashboards (API usage, provider health, user activity) |
| Prometheus | `http://host:9090` | Metrics collection |
| Health endpoint | `GET /api/v1/health` | Quick status check |
| Health services | `GET /api/v1/health/services` | Individual service status |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Backend unhealthy | Redis not responding | `docker compose restart redis` |
| Frontend crash loop | Missing node_modules | `docker compose exec frontend npm install` |
| Stripe checkout fails | Missing STRIPE_SECRET_KEY | Check `.env` has live keys |
| Rate limiting too strict | Redis cleared | Check `RATE_LIMIT_PER_MINUTE` in `.env` |
| Database connection fail | Postgres not ready | Wait 30s, docker compose logs postgres |

## Updating

```bash
git pull origin main
docker compose up -d --build
docker compose exec backend alembic upgrade head  # if new migrations
```

## Rollback

```bash
git revert HEAD
docker compose up -d --build
```
