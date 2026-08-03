# Incident Response Playbook

## Severity Levels
- **P0**: Platform down, data loss, active breach
- **P1**: Feature broken, degraded performance
- **P2**: Minor bug, cosmetic issue
- **P3**: Enhancement request

## Incident Response Process

### 1. Detection
- Prometheus alerts in Grafana
- Sentry error rate spikes
- User reports via support

### 2. Triage (5 min)
1. Confirm incident severity
2. Assign incident commander
3. Create incident channel

### 3. Mitigation (15 min)
1. Rollback to last stable deploy
2. Feature flag disable
3. Scale up resources

### 4. Resolution
1. Root cause analysis
2. Fix and test in staging
3. Deploy with monitoring

### 5. Post-mortem
1. Timeline document
2. Action items
3. Update runbook

## Key Contacts
- **Infra on-call**: #infra-alerts
- **Security**: security@miau.finance
- **Escalation**: CTO on-call
