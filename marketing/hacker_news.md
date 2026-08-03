# Show HN: Miau Finance — Proprietary terminal for stocks, crypto, DeFi (v1.0.0)

Hey HN,

For the past 2 years I've been building **Miau Finance** — a cat-themed, terminal-based financial analytics platform. It's proprietary commercial, hosted, and tries to be what Bloomberg Terminal would look like if it were built by someone who really likes cats.

**What it does in one terminal:**
- Real-time stocks, crypto, forex, options
- 6 broker integrations (Alpaca, IBKR, Saxo, DEGIRO, Rakuten, Zerodha)
- WalletConnect v2 + 7 blockchains + Uniswap/Aave/Curve/Lido/Maker/Yearn
- DCF, WACC, LBO, Comparable Analysis
- Monte Carlo simulation, VaR, Greeks, regime detection
- ESG scoring + carbon footprint tracking
- AI advisor with NLP + autonomous trading agents
- NFT portfolio tracker (floor prices, rarity scoring, marketplace APIs)
- Plugin system + Python/JS SDKs + curl examples

**Stack:**
Python/FastAPI, React/TypeScript terminal UI, Rust PyO3, PostgreSQL, Redis, 10 Docker containers, K8s manifests included. 120+ API endpoints.

**Why cats?**
Finance is stressful. Your terminal should not add to it. Error messages like "😹 404 — the cat hid it" and "🐈 429 — rate limited, the cat needs a nap" make debugging slightly more bearable.

**The numbers:**
- 27 phases of development
- 400+ commits
- 260+ tests passing
- MIAU EULA

**Try it:**
```bash
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd miau-finance
docker compose up -d
```

Then open your terminal and type `miau` — or hit port 5173 for the web UI.

I'd love your feedback. The cat demands it. 🐱

GitHub: https://github.com/LuZziD/cat-finance-analytics-shell-miau
