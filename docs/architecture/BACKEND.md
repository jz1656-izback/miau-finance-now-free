# 🐱 MIAU FINANCE — Backend Architecture

## FastAPI · Async SQLAlchemy · PostgreSQL · Redis · 515+ Endpoints

### Directory Structure
```
backend/app/
├── main.py          # Entry + all router registrations
├── config.py        # Environment config
├── database.py      # SQLAlchemy async setup
├── api/             # 50+ route handler files
│   ├── billing.py   # Stripe, pricing, crypto payments
│   ├── wealth.py    # Wealth management
│   ├── jobs_api.py  # Job search
│   ├── treasury.py  # Fixed income
│   └── ...
├── services/        # Business logic
│   ├── revenue.py   # 10/80/10 split tracking
│   ├── treasury_manager.py
│   ├── wealth_engine.py
│   ├── auto_investor.py
│   ├── crypto_payments.py
│   ├── analytics/   # Technicals, econometrics, risk
│   ├── brokers/     # Alpaca, IBKR
│   └── data/        # 50+ data providers
├── middleware/       # 11 middleware layers
└── models/          # All SQLAlchemy models
```

### Architecture Highlights
- **Async everywhere**: FastAPI + async SQLAlchemy + httpx
- **Provider pattern**: Every external API wrapped as DataSource
- **3-tier revenue**: 10% ops / 80% hooman / 10% cats
- **11 middleware layers**: CORS, Auth, Rate Limit, Tier, CSRF, Audit...
- **Tier enforcement**: Free=30/min, Pro=300/min, Enterpriser=10K/min
