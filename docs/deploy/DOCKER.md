# 🐱 MIAU FINANCE — Docker Reference

## Profiles
| Profile | RAM | Services |
|---------|-----|----------|
| **Light (dev)** | ~200 MB | postgres, redis, backend, frontend |
| **Full** | ~5 GB | + grafana, superset, prometheus, minio |

## Commands
```bash
# Light mode (recommended)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Full mode
docker compose up -d

# Logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart
docker compose restart backend

# Stop all
docker compose down

# PostgreSQL CLI
docker compose exec postgres psql -U miau

# Rebuild
docker compose build frontend

# Clean all (⚠️ deletes data)
docker compose down -v
```

## Dockerfile (Frontend)
```dockerfile
FROM node:20-alpine AS builder        # Production build
FROM node:20-alpine AS development     # Dev with hot reload
FROM nginx:alpine AS production        # Static file serving
```
