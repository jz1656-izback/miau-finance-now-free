# 🐱 Miau Finance — Complete Tutorial

> *"The cat doesn't care about your sprint velocity. The cat only cares that you shipped."*

---

## 📋 Table of Contents
1. [Quick Start](#-quick-start)
2. [Terminal Basics](#-terminal-basics)
3. [Data Sources & API Keys](#-data-sources--api-keys)
4. [MiauGlobe 3D Earth](#-miauglobe-3d-earth)
5. [World Map (2D)](#-world-map-2d)
6. [3D Charts (Three.js)](#-3d-charts-threejs)
7. [Miau Finance Vault](#-miau-finance-vault)
8. [Log Viewer](#-log-viewer)
9. [MiauBook (Social Feed)](#-miaubook-social-feed)
10. [Admin Dashboard](#-admin-dashboard)
11. [Rust Analytics Engine](#-rust-analytics-engine)
12. [Cat Galaxy](#-cat-galaxy)

---

## 🚀 Quick Start

### Prerequisites
- Docker 24+ with Compose V2
- Node.js 20+ (for frontend dev)
- Python 3.12+ (for backend dev)

### 1. Clone & enter
```bash
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd miau-finance
export REPO_ROOT=$(pwd)
```

### 2. Start backend services
```bash
docker compose up -d postgres redis backend
# Wait ~10s for DB to init, then:
curl http://localhost:8000/api/v1/health
```

### 3. Start frontend
```bash
cd frontend
npm install
npx vite --host 0.0.0.0 --port 5173
# Opens http://localhost:5173
```

### 4. Log in
```
login admin miau2026
```

### 5. First commands
```
help          # list all commands
price AAPL    # get live stock price
miaumap       # open 3D globe
chart3d AAPL  # 3D candlestick chart
cat           # pet the cat
```

---

## 💻 Terminal Basics

The terminal is the primary interface. Type any command and press Enter.

### Navigation
| Command | Description |
|---------|-------------|
| `help` | List all available commands |
| `help <category>` | Filter by category (market, portfolio, etc.) |
| `clear` | Clear terminal screen |
| `history` | Show command history |
| `↑↓` | Cycle through command history |
| `Ctrl+F` | Search terminal output |

### System Info
| Command | Description |
|---------|-------------|
| `whoami` | Show current user |
| `date` | Current date/time |
| `time` | Market time and status |
| `status` | Personal dashboard — tier, tuna, streak |

---

## 🔑 Data Sources & API Keys

### Supported Providers
| Provider | Key Env Var | Data |
|----------|------------|------|
| **Finnhub** | `FINNHUB_API_KEY` | Stock quotes, fundamentals, SEC filings |
| **Twelve Data** | `TWELVEDATA_API_KEY` | Real-time data, technical indicators |
| **FRED** | `FRED_API_KEY` | Macroeconomic data (GDP, CPI, employment) |
| **EIA** | `EIA_API_KEY` | Energy data, petroleum, renewables |
| CoinGecko | *(no key needed)* | Crypto prices |
| SecuritiesDB | *(no key needed)* | Piotroski F-Score, Altman Z |
| BlockNative | *(no key needed)* | Ethereum mempool |

### Adding API Keys

**Option 1: Edit `.env` file**
```bash
nano .env
# Add your keys, then restart backend:
docker compose up -d backend
```

**Option 2: Use the encrypted vault**
```bash
bash scripts/setup-api-keys.sh
```

---

## 🌍 MiauGlobe 3D Earth

The MiauGlobe is a full Three.js 3D interactive globe with 12 live data layers. It replaces the earlier globe.gl library for better performance and control.

### Opening the Globe
```
miaumap                    # Open globe
miaumap --cats             # Globe with cat army layer
miaumap --aliens           # Globe with UFO hotspots (unlocked via x-files)
```

### Controls
- **Drag** to rotate
- **Scroll** to zoom
- **Click markers** for info panels
- **ESC** to close

### Data Layers
1. Aviation (live aircraft)
2. Maritime (ships)
3. Military (bases)
4. Mining (operations)
5. Corporate (top 500 companies as cat sprites)
6. Satellite (ISS, Starlink, spy sats)
7. UFO / Aliens (18 hotspot locations)
8. Conflicts (simulated)
9. Cargo (trade routes)
10. Night / Terrain
11. Cats (cat army marching)
12. Spy satellites (6 "CLASSIFIED")

### Color Legend
| Color | Meaning |
|-------|---------|
| Green ▲ | Stock up |
| Red ▼ | Stock down |
| Purple | M&A deal arc |
| Magenta | UFO sighting heatmap |
| Blue | Satellite orbit |

---

## 🗺️ World Map (2D)

The Leaflet-based 2D map provides a traditional view:
```
map           # toggle 2D map
```

Features: zoom/scroll, marker clusters, CDN fallback chain.

---

## 📊 3D Charts (Three.js)

Three interactive 3D charting tools, all using pure Three.js (no globe.gl):

### 3D Candlestick Chart
```
chart3d <ticker>       # Open 3D candlestick chart
S key                  # Take screenshot
ESC                    # Close
```
Features: volume bars, period selector, orbit controls, wick rendering.

### 3D IB Dashboard (4-panel)
```
sheetz3d <ticker>      # Open DCF + WACC + Comps + LBO in 3D
```
Each panel is a Three.js scene with orbit controls.

### 3D Comparison
```
compare3d <t1> <t2>    # Multi-ticker 3D line comparison
```
All 3D charts are locked behind Pro tier.

---

## 🔐 Miau Finance Vault

The vault stores API keys using Fernet AES-256-GCM encryption at rest.

```
vault              # Open vault (if accessible from terminal)
```

Used by 5 providers: Finnhub, TwelveData, BLS, CoinPaprika, Etherscan.
Keys persist to `backend/data/key_vault.json`.

---

## 📋 Log Viewer

Centralized log viewer for all Docker services:
```
logs               # Open log viewer
```
Supports: service filtering, search within logs, auto-refresh.

---

## 📱 MiauBook (Social Feed)

```
MiauBook            # Social trading feed
```
Features: global feed, following system, likes, comments, portfolio sharing.

---

## 🖥️ Admin Dashboard

```
admin               # Admin panel
```
Team management, billing overview, API key usage, user activity.

---

## 🦀 Rust Analytics Engine

The Rust PyO3 engine provides accelerated quantitative finance:

```bash
cd backend/rust_analytics
cargo build --release
# Available via Python: from app.services.rust_bridge import *
```

Features: Black-Litterman portfolio optimization, Fama-French factor models.

---

## 🐱 Cat Galaxy

Easter egg features cat-themed bonuses:

| Command | Effect |
|---------|--------|
| `cat` | Random ASCII cat art (28 breeds) |
| `cat --dance` | Dancing cat disco 🎵 |
| `cat --gang` | 5-cat crew rolls deep |
| `cat --party` | Party cats with confetti 🎉 |
| `cat --fortune` | Financial wisdom from the cat |
| `cat --adopt` | Adopt a terminal cat |

---

## 📚 Reference

| Doc | What |
|-----|------|
| [COMMANDS.md](COMMANDS.md) | Terminal command reference (193 commands) |
| [API.md](API.md) | REST API reference (515+ endpoints) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [SECURITY.md](SECURITY.md) | Security, PQC, rate limiting |
| [MONETIZATION.md](MONETIZATION.md) | Pricing and revenue model |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute quick start |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production deployment |
| [DEVELOPER.md](DEVELOPER.md) | Developer guide |
| [COMPLIANCE](compliance/) | BaFin/GDPR compliance |
