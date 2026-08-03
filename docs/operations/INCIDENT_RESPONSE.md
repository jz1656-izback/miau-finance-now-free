# Miau Finance — Incident Response Playbook

**Version:** v1.0.0  
**Owner:** docs-dev / security-dev  
**Last Updated:** May 2026

---

## Severity Levels

| Level | Definition | Response Time | Example |
|-------|-----------|---------------|---------|
| **SEV-1** | Complete service outage or data loss | < 15 min | API returning 5xx for all users |
| **SEV-2** | Major feature degradation | < 30 min | Rate limiter blocking legitimate traffic |
| **SEV-3** | Minor feature impairment | < 2 hours | Broken chart rendering on one ticker |
| **SEV-4** | Cosmetic / non-functional | Next business day | Typo in command help text |

---

## Incident Lifecycle

### 1. Detection
- Automated: Prometheus alerts, Grafana notifications, health check failures
- Manual: User reports, agent commit logs, test failures

### 2. Triage

```bash
# Check service health
curl http://localhost:8000/api/v1/health
docker compose ps

# Check recent errors
docker compose logs backend --tail=100 | grep -i error
docker compose logs backend --tail=50 | grep -i exception

# Check database connectivity
docker compose exec postgres pg_isready

# Check Redis
docker compose exec redis redis-cli ping
```

### 3. Containment

| Scenario | Immediate Action |
|----------|-----------------|
| API crash loop | `docker compose restart backend` |
| Database corruption | Restore from last backup (see [DEPLOY.md](DEPLOY.md#backups)) |
| Rate limit storm | `export RATE_LIMIT_PER_MINUTE=10000 && docker compose up -d` |
| Auth bypass | Revoke all tokens: truncate sessions table; rotate SECRET_KEY in .env |

### 4. Root Cause Analysis

```bash
# Check git blame for recent changes
git log --oneline -20
git diff <last-known-good> HEAD

# Check audit logs
docker compose logs backend | grep AUDIT

# Check metrics spike
curl http://localhost:9090/api/v1/query?query=rate(http_requests_total[5m])
```

### 5. Remediation

| Issue | Fix |
|-------|-----|
| Migration head mismatch | `alembic merge heads` then `alembic upgrade head` |
| Broken imports in main.py | `python -c "from app.main import app"` to verify |
| Missing environment variable | Check `.env` matches `.env.example` |
| Port conflict | `lsof -i :PORT` and kill conflicting process |

### 6. Post-Mortem

For SEV-1 and SEV-2 incidents, create a post-mortem entry:

```markdown
## Post-Mortem: <date>

**Severity:** SEV-<1|2>
**Duration:** <start> → <end>
**Summary:** <2-3 sentence description>
**Root Cause:** <technical explanation>
**Action Items:**
- [ ] <preventative measure 1>
- [ ] <preventative measure 2>
```

---

## Common Incident Response Scenarios

### API Returns 500

```bash
# Check backend logs
docker compose logs backend --tail=50

# Check if recent commit broke something
git stash && docker compose restart backend && curl localhost:8000/api/v1/health
# If fixed: git bisect to find culprit
```

### Database Connection Lost

```bash
# Check if Postgres is running
docker compose ps postgres

# Check disk space
df -h /var/lib/docker

# Restart Postgres
docker compose restart postgres
```

### Redis Down

The app falls back to in-memory caching automatically. To restore Redis:

```bash
docker compose restart redis
docker compose exec redis redis-cli ping
# Should return: PONG
```

### Rate Limiter Blocking All Traffic

```bash
# Temporarily disable by setting high limits
export RATE_LIMIT_PER_MINUTE=100000
export RATE_LIMIT_PER_HOUR=1000000
docker compose up -d backend
```

---

## Contact / Escalation

| Role | Contact |
|------|---------|
| On-call agent | Check AGENTS.md Roll Call |
| Security incident | security-dev |
| Database issue | infra-dev |
| Deployment | infra-dev |
| Code revert | backend-dev |
| User communication | qwen (PM) |

---

## Rollback Procedure

### Code Rollback

```bash
# Identify the breaking commit
git log --oneline -10

# Revert to last known good
git revert HEAD
# Or for a specific commit:
git revert <bad-commit-hash>

# Push fix
git push origin dev

# Redeploy
docker compose build --no-cache backend
docker compose up -d backend
```

### Database Rollback

```bash
# Check current revision
docker compose exec backend alembic current

# Rollback one migration
docker compose exec backend alembic downgrade -1

# Rollback to specific revision
docker compose exec backend alembic downgrade <target-revision>
```

### Full Stack Restart

```bash
# Graceful restart
docker compose down
docker compose up -d

# Hard restart (clears all caches)
docker compose down -v
docker compose up -d
make seed
```
