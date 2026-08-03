# 🐱 Miau Apps — Ecosystem Overview

The `apps/` directory contains all standalone web applications in the Miau Finance ecosystem.
Each app is self-contained, has its own login via **Pawdenity**, and shares the same JWT token.

| App | Port | Description | Tech |
|-----|------|-------------|------|
| **🏢 Miau Corp** | 5175 | Corporate ecosystem site, pricing, products, cat cabinet | Vanilla HTML/CSS/JS + Vite |
| **🎓 Education Platform** | 5174 | 230 courses, 18 certifications, 5 career tracks | React + Vite + Tailwind |
| **📊 Marketing Dashboard** | 5176 | Analytics, campaigns, SEO, traffic, conversions | React + Vite + Recharts |
| **🚒 Service Desk** | 5180 | Ticket system, cat firefighters, system status | Vanilla HTML/CSS/JS |
| **🐾 Pawdenity** | 5190 | Central auth provider — one account, all tools | Vanilla HTML/CSS/JS |
| **📊 CeoScratchSheet** | 5182 | Unified ecosystem dashboard — all metrics one page | Vanilla HTML/CSS/JS |
| **🚀 Landing Page** | 8080 | Cat rocket marketing page, product links | Vanilla HTML/CSS/JS |

## Quick Start

```bash
# Start all apps (each in its own terminal):
cd apps/ecosystem-site       && npm run dev    # 5175
cd apps/education-platform   && npm run dev    # 5174
cd apps/marketing-dashboard  && npm run dev    # 5176
python3 -m http.server 5180 --directory apps/service-desk/   # 5180
python3 -m http.server 5190 --directory apps/auth/           # 5190
python3 -m http.server 8080 --directory apps/landing-page/   # 8080
```

## Authentication

All apps use the same auth system:
- **Login:** `POST /api/v1/auth/token` (username + password → JWT)
- **Register:** `POST /api/v1/auth/register` (email + username + password)
- **Token:** Stored in `localStorage` as `miau_token`, sent as `Authorization: Bearer`
- **Superadmin:** `pawdmin` / `miau2026`

Login once on Pawdenity (port 5190) and the token broadcasts to all apps via the backend relay.
