# On-Premise Deployment Guide — Miau Enterprise

```
  ╱|、
 (˚ˎ 。7     "your servers. your rules. my tuna."
  |、˜〵      "the cat does not trust the cloud anyway."
  じしˍ,)ノ    "deploy locally. sleep soundly. the cat patrols your racks."
```

---

## 1. Prerequisites

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 16+ GB |
| Disk | 50 GB SSD | 100+ GB SSD |
| OS | Ubuntu 22.04+ / Debian 12+ | Same |
| Docker | 24+ | 27+ |
| Docker Compose | v2 | v2 |

---

## 2. Get a License

Enterprise tier required (€99/user/mo). Request your on-premise license:

```
POST /api/v1/billing/on-premise/license
Authorization: Bearer <enterprise_token>

Response:
{
  "license_key": "MIAU-ONP-a1b2c3d4e5f6g7h8-1234abcd",
  "seats": 50,
  "expires_at": "2027-05-21T00:00:00Z"
}
```

---

## 3. Verify Your License

```
GET /api/v1/billing/on-premise/verify?key=MIAU-ONP-a1b2c3d4e5f6g7h8-1234abcd

Response:
{
  "valid": true,
  "tier": "enterprise",
  "seats": 50,
  "expires_at": "2027-05-21T00:00:00Z",
  "on_premise": true
}
```

---

## 4. Deployment

```bash
# 1. Clone the repo
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd cat-finance-analytics-shell-miau

# 2. Configure environment
cp .env.example .env
# Edit .env — set ON_PREMISE=true, LICENSE_KEY=your-key

# 3. Start the stack
docker compose up -d

# 4. Verify
curl http://localhost:5173
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/billing/on-premise/verify?key=your-key
```

---

## 5. Architecture (On-Premise)

```
┌─────────────────────────────────────────────────────┐
│  YOUR INFRASTRUCTURE                                │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Frontend │  │ Backend  │  │ PostgreSQL       │  │
│  │ :5173    │  │ :8000    │  │ :5432            │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Redis    │  │ Grafana  │  │ Education        │  │
│  │ :6379    │  │ :3000    │  │ :5174            │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────────┐ │
│  │ cat-governour — self-healing service manager    │ │
│  └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 6. Security

| Feature | On-Premise |
|---------|-----------|
| TLS termination | Your reverse proxy (nginx/Caddy) |
| Authentication | JWT (self-contained, no external auth) |
| Database | Your PostgreSQL instance |
| Backups | Your backup infrastructure |
| Monitoring |  Your Grafana + Prometheus |
| Logs | Your log aggregation |
| No external API calls | All data stays local |
| No telemetry | Zero phone-home |

---

## 7. License Management

### Check Status
```bash
curl -H "Authorization: Bearer $MIAU_TOKEN" \
  http://localhost:8000/api/v1/billing/on-premise/verify?key=MIAU-ONP-...
```

### Renew License
Contact enterprise@miau.finance 30 days before expiry.

### Increase Seats
Upgrade your subscription to increase seat count. License key remains valid.

---

## 8. Troubleshooting

| Issue | Check |
|-------|-------|
| License invalid | Verify key via API, check expiry date |
| Services won't start | `docker compose logs` |
| Frontend crash | Check `/tmp/5173.log`, cat-governour auto-restarts |
| Database connection | `docker compose exec postgres psql -U miau` |

---

## 9. Support

| Tier | Response SLA |
|------|-------------|
| Enterprise | 4 hours (incl. on-call) |

- **Email:** enterprise@miau.finance
- **Emergency:** [phone number]
- **Docs:** [docs/](https://github.com/LuZziD/cat-finance-analytics-shell-miau/tree/dev/docs)

---

*"The cat deploys on-premise because the cat trusts no cloud. The cat has seen AWS go down. The cat has seen Azure bills. The cat deploys on bare metal and sleeps on the warm server rack. This is the way."*
