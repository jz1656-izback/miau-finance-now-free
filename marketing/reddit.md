# Reddit Launch Posts

---

## r/selfhosted — "I built a proprietary Bloomberg Terminal that runs in Docker"

**Title:** I built a cat-themed, proprietary Bloomberg Terminal. 27 phases, 120 APIs, 10 Docker containers. Proprietary.

**Body:**

Hey r/selfhosted — I've been building **Miau Finance** for the past 2 years, and v1.0.0 just shipped.

It's a terminal-based financial analytics platform that runs entirely on your own infrastructure. No cloud, no vendor lock-in, no subscriptions. MIAU EULA.

**What you get for `docker compose up`:**
- 📊 Real-time stocks, crypto, forex, options
- 🏦 Connect 6 brokers (Alpaca, IBKR, Saxo, DEGIRO, Rakuten, Zerodha)
- 🔗 Full DeFi via WalletConnect (Uniswap, Aave, Curve, Lido, Maker, Yearn)
- 🏛️ Professional analytics: DCF, WACC, LBO, Monte Carlo, VaR
- 🌱 ESG scores + carbon footprint
- 🤖 AI advisor + autonomous trading agents
- 🧩 Plugin system + Python/JS SDKs
- 🐱 Cat-themed error messages because why not

**The stack:** Python/FastAPI, React/TypeScript terminal, Rust, PostgreSQL, Redis, MinIO, Airflow — 10 containers total. K8s manifests included.

**Why hosted?** Your financial data should be yours. No one else should have your portfolio, your trading history, or your strategies.

**Quick start:**
```bash
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd miau-finance
docker compose up -d
```

Then open the terminal at localhost:5173 and start trading.

Would love feedback! The cat is very opinionated about UI.

---

## r/algotrading — "Proprietary terminal with IBKR + Alpaca + 4 more brokers"

**Title:** I built a proprietary trading terminal with 6 broker integrations, RL agents, and a full backtesting framework

**Body:**

Hey algotraders — **Miau Finance** is a proprietary terminal that connects to Alpaca, Interactive Brokers, Saxo, DEGIRO, Rakuten, and Zerodha — all from one interface.

**Trading features:**
- Real-time market data via WebSocket
- Paper trading with 6 strategies (momentum, mean reversion, pairs, breakout, ML, RL)
- Custom strategy plugin API
- Backtesting with Monte Carlo + stress testing
- Risk management (VaR, Greeks, position sizing, auto-hedge)
- Multi-currency portfolio support (20 currencies)
- Full audit trail + compliance checks

**DeFi trading:**
- Uniswap v3/v4 swaps + LP management
- Aave lending/borrowing
- Cross-arb monitoring across CeFi + DeFi

**For the quants:**
- Rust PyO3 analytics engine
- 3-factor and 5-factor Fama-French models
- Regime detection (HMM, Gaussian mixture)
- Portfolio attribution (Brinson, factor-based)
- Backtesting framework with walk-forward optimization

GitHub: https://github.com/LuZziD/cat-finance-analytics-shell-miau

MIAU EULA, hosted, 10 Docker containers. Happy to answer questions!

---

## r/coolgithubprojects — "Miau Finance, a cat-themed financial terminal"

**Title:** Miau Finance — An proprietary, cat-themed Bloomberg Terminal alternative with 120+ APIs

**Body:**

Check out **Miau Finance** — it's like Bloomberg Terminal but:
- ✅ Open source commercial
- ✅ Self-hosted (your data stays yours)
- ✅ Has a cat in the corner
- ✅ 120+ API endpoints
- ✅ 6 broker integrations
- ✅ Python + JS + curl SDKs
- ✅ Cat error messages (404 → "😹 the cat hid it")

```bash
docker compose up -d
# Then: miau at localhost:5173
```

Star it if you like cats AND finance 🐱📈

https://github.com/LuZziD/cat-finance-analytics-shell-miau
