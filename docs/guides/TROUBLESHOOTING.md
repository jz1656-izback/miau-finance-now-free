# 🐱 MIAU FINANCE — Troubleshooting

## Common Issues & Fixes

### "Container keeps restarting"
```bash
docker compose logs frontend | tail -50
# Likely: npm install failing
docker compose down
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### "Backend unhealthy"
```bash
docker compose logs backend | tail -20
# Wait 30s for PostgreSQL or check .env vars
docker compose restart backend
```

### "Port already in use"
```bash
sudo lsof -i :5173  # frontend
sudo lsof -i :8000  # backend
sudo lsof -i :5434  # postgres
```

### "MIAU EATS MY RAM"
Full stack uses ~5 GB. Use light mode:
```bash
docker compose down
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
# Now ~200 MB
```

### "Error overlay in browser"
Stale Vite HMR error. Press Esc or hard refresh (Ctrl+Shift+R).

### "API returns 401"
Login first: `login demo demo@miau.finance miau2026`

### "No data for ticker"
Yahoo Finance rate limited. Wait 30s and retry.

### Still stuck?
Open an issue at https://github.com/LuZziD/cat-finance-analytics-shell-miau/issues
# 🐱 MIAU FINANCE — Troubleshooting Guide

## Quick Fixes for Common Problems

### Terminal Shows Red Error Overlay
**Problem**: Vite HMR overlay showing syntax/runtime errors
**Fix**: 
1. Press `Esc` to dismiss overlay
2. Hard refresh: `Ctrl+Shift+R`
3. Check terminal for actual build errors

### MIAU EATS MY RAM
**Problem**: Full docker stack uses ~5 GB RAM
**Fix**: Use light mode:
```bash
docker compose down
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
# Now ~200 MB
```

### Container Won't Start
```bash
# Check logs
docker compose logs backend | tail -30
docker compose logs frontend | tail -30
docker compose logs postgres | tail -30

# Common fixes:
# postgres: set POSTGRES_PASSWORD in .env
# backend: wait for postgres to be healthy
# frontend: npm install failing? Check network
```

### "No data for ticker"
**Problem**: Yahoo Finance rate limited
**Fix**: Wait 30s and retry. Add API keys for redundancy.

### Checkout Fails
**Problem**: "Checkout failed" or 401 on billing
**Fix**:
1. Login first: `login demo demo@miau.finance miau2026`
2. Check Stripe keys are configured in .env
3. Try test mode: use Stripe test card `4242 4242 4242 4242`

### "Feature requires Pro"
**Problem**: AI commands blocked on free tier
**Fix**: Type `billing upgrade` to subscribe, or start a 7-day trial with `billing trial`

### Database Connection Error
```bash
# Check if postgres is running
docker compose ps postgres
# Restart if unhealthy
docker compose restart postgres
```

### Built by One Developer
This is a one-person project. Issues are fixed as fast as the cat can type. Open a GitHub issue if you find a bug.

> *"The cat fixed it. The cat documented the fix. The cat moves on." 🐱*
# 🐱 MIAU FINANCE — Troubleshooting Guide

## Quick Fixes for Common Problems

### Terminal Shows Red Error Overlay
**Problem**: Vite HMR overlay showing syntax/runtime errors
**Fix**: 
1. Press `Esc` to dismiss overlay
2. Hard refresh: `Ctrl+Shift+R`
3. Check terminal for actual build errors

### MIAU EATS MY RAM
**Problem**: Full docker stack uses ~5 GB RAM
**Fix**: Use light mode:
```bash
docker compose down
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
# Now ~200 MB
```

### Container Won't Start
```bash
# Check logs
docker compose logs backend | tail -30
docker compose logs frontend | tail -30
docker compose logs postgres | tail -30

# Common fixes:
# postgres: set POSTGRES_PASSWORD in .env
# backend: wait for postgres to be healthy
# frontend: npm install failing? Check network
```

### "No data for ticker"
**Problem**: Yahoo Finance rate limited
**Fix**: Wait 30s and retry. Add API keys for redundancy.

### Checkout Fails
**Problem**: "Checkout failed" or 401 on billing
**Fix**:
1. Login first: `login demo demo@miau.finance miau2026`
2. Check Stripe keys are configured in .env
3. Try test mode: use Stripe test card `4242 4242 4242 4242`

### "Feature requires Pro"
**Problem**: AI commands blocked on free tier
**Fix**: Type `billing upgrade` to subscribe, or start a 7-day trial with `billing trial`

### Database Connection Error
```bash
# Check if postgres is running
docker compose ps postgres
# Restart if unhealthy
docker compose restart postgres
```

### Built by One Developer
This is a one-person project. Issues are fixed as fast as the cat can type. Open a GitHub issue if you find a bug.

> *"The cat fixed it. The cat documented the fix. The cat moves on." 🐱*
---\n*Merged from TROUBLESHOOTING_QUICK.md (V69 The Great Delittering)*\n

---
*Merged from TROUBLESHOOTING_QUICK.md during V69 The Great Delittering*

