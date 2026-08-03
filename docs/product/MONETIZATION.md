# 🐱 MIAU FINANCE — Monetization Guide

## Revenue Model
```
100% Revenue
  ├── 10% → 🔧 Operating Fund (servers, fees, cloud)
  ├── 80% → 🦜 Hooman → ziebartjevgeni@gmail.com
  └── 10% → 🐱 Cat Ecosystem (auto-invested)
```

## Pricing

> 🚧 **90% development discount active** — valid until May 2027. We're still in development. Prices will return to normal after 1 year.

| Tier | Development Price | Original Price | Rate Limit | Features |
|------|------------------|---------------|------------|----------|
| Free | €0 | €0 | 30/min | Basic market data |
| Pro | **€9.90/mo** 🎉 | ~~€99/mo~~ | 300/min | AI advisor, paper trading |
| Tiny Catfunds | **€1.90/mo** 🎉 | ~~€19/mo~~ | 1K/min | Teams, 3 barks/yr |
| Enterprise | **€39.60/mo** 🎉 | ~~€396/mo~~ | 10K/min | Custom deployment, SLA |

## Revenue Scenarios (Development Pricing)
| Customers | Monthly (Pro €9.90) | Hooman Gets (80%) |
|-----------|--------------------|-------------------|
| 1 | €9.90 | €7.92 |
| 5 | €49.50 | €39.60 |
| 10 | €99.00 | €79.20 |
| 50 | €495.00 | €396.00 |
| 500 | €4,950.00 | €3,960.00 |

## Revenue Scenarios (Full Pricing — after May 2027)
| Customers | Monthly (Pro €99) | Hooman Gets (80%) |
|-----------|------------------|-------------------|
| 1 | €99 | €79 |
| 5 | €495 | €396 |
| 10 | €990 | €792 |
| 50 | €4,950 | €3,960 |
| 500 | €49,500 | €39,600 |

## Go-Live Checklist
1. Create Stripe account → API keys
2. Create products: Pro €99/mo, Enterprise €396/mo
3. Fill `.env.go-live` → rename to `.env`
4. Restart backend
5. Make public via ngrok or VPS
6. Share URL (see scripts/marketing-copy.txt)

## Track Revenue
```bash
miaucfo    # Full dashboard
miauwealth # Net worth
```

**Break-even: 1 customer. Everything after is profit.**
