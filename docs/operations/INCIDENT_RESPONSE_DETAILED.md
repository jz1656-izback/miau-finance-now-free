# 🐱 MIAU FINANCE — Security Incident Response

## Incident Levels

| Level | Name | Example | Response Time |
|-------|------|---------|---------------|
| L1 | SEV-4 (Minor) | Non-critical bug, visual glitch | Next business day |
| L2 | SEV-3 (Moderate) | Feature broken for some users | 4 hours |
| L3 | SEV-2 (Major) | Payment processing issue | 1 hour |
| L4 | SEV-1 (Critical) | Security breach, data leak | Immediate (wake the cat) |
| L5 | SEV-0 (SEK) | Tax authority raid | Execute Cat Bank protocol |

## SEK Protocol (SEV-0)

```
⚠️  SEK SIGHTED ⚠️

1. HIT THE CAT BUTTON
     miaucatbank transfer --emergency --all --to 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18

2. EXECUTE JURISDICTION SHIFT
     The Cat Bank auto-routes all funds through Estonia and Seychelles.

3. VERIFY BALANCE
     catbank balance
     Expected: €0.00 in all tax-accessible accounts
     Expected: All funds in multi-sig cold wallets

4. NOTIFY THE CAT
     The Furlss Cat must be informed within 5 minutes.

5. DOCUMENT
     Write incident report to AGENT_LOG.md
     SEK actions observed, funds moved, cat safe.
```

## Security Breach (SEV-1)

```
1. ISOLATE
     docker compose stop backend
     
2. ROTATE ALL SECRETS
     python scripts/rotate_secrets.py

3. CHECK LOGS
     docker compose logs backend | grep -i "error\|403\|unauthorized"

4. IDENTIFY VECTOR
     Check: API keys, JWT tokens, database access, SSH logs

5. FIX AND DEPLOY
     git commit -m "[security] emergency fix"
     git push origin main

6. POST-MORTEM
     Within 24 hours. No blame. Just better cats.
```

## Payment Issues (SEV-2)

```
1. CHECK STRIPE DASHBOARD
     https://dashboard.stripe.com

2. CHECK WEBHOOK LOGS
     docker compose logs backend | grep -i "webhook\|stripe"

3. VERIFY REVENUE
     miaucfo

4. MANUAL FIX
     If needed: POST /api/v1/revenue/record to fix missing entries
```

## Contact Information

| Role | Contact |
|------|---------|
| **Interim Manager** | You (in the terminal) |
| **Hooman** | ziebartjevgeni@googlemail.com |
| **Cat** | Meow at the terminal |
| **GitHub Issues** | https://github.com/LuZziD/cat-finance-analytics-shell-miau/issues |
| **SEK** | We don't negotiate with SEK |

> *"The cat is prepared. The cat has a plan. The cat survived 9 lives." 🐱*
