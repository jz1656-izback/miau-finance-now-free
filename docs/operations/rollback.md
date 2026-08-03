# Rollback Procedure

## Quick Rollback (Docker)
```bash
# Rollback to previous version
docker compose down
docker compose up -d

# If using tags:
docker compose pull backend:v1.0.0-previous
docker compose up -d
```

## K8s Rollback
```bash
# Check rollout history
kubectl rollout history deployment/backend

# Rollback to previous
kubectl rollout undo deployment/backend

# Rollback to specific revision
kubectl rollout undo deployment/backend --to-revision=3

# Verify
kubectl rollout status deployment/backend
```

## Database Rollback
```bash
# Run Alembic downgrade
cd backend && alembic downgrade -1

# Or to specific migration
cd backend && alembic downgrade <revision_id>
```

## Frontend Rollback
```bash
# Vite build rollback
cd frontend && git checkout <previous-deploy-tag>
npm run build
```

## Post-Rollback Checklist
1. Verify health endpoint returns 200
2. Run smoke test suite
3. Check error rates in Grafana
4. Confirm database migrations are consistent
5. Notify users via status page
