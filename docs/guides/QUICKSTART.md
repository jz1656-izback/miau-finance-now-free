# Miau Finance Quickstart — 🐱 Meow or Die

```
  ╱|、
 (˚ˎ 。7     "you have 5 minutes. the cat has less patience."
  |、˜〵      "bloomberg costs $24k/yr. miau costs $0."
  じしˍ,)ノ    "type fast. the cat is watching."
```

---

## 1. Open the Terminal

```
http://localhost:5173
```

No signup? Type: `login admin miau2026`

---

## 2. Your First 5 Commands

| Command | What it does | Cat says |
|---------|-------------|----------|
| `price AAPL` | Latest Apple price | "The cat bought AAPL at $12. The cat is up 16,000%." |
| `market` | Market overview | "Everything is either green or the cat's color-blind." |
| `ta AAPL` | Technical indicators | "The cat sees patterns humans don't. RSI says: nap." |
| `cat` | Pet the cat | "The cat accepts your offering." |
| `help` | All 160+ commands | "The cat has written more documentation than you've read." |

---

## 3. Core Categories

```
📈  MARKET DATA    → price, quote, market, index, crypto, fx
📊  ANALYTICS       → ta, risk, correl, ols, granger, capm
💼  PORTFOLIO       → portfolio, buy, sell, pnl, holdings
🤖  AI              → advisor, sentiment, predict, miau-ai
🌍  GLOBE           → map, satellite, military, mining, aliens
💳  BILLING         → billing, pricing, subscribe
🐱  FUN             → cat, joke, rave, tuna, meow, veto
```

---

## 4. Pricing (Yes, the Cat Charges)

| Tier | Development Price | Original Price | What you get |
|------|-------------------|---------------|-------------|
| **Free** | €0 | €0 | Basic commands, 30 req/min |
| **Pro** | **€9.90/user/mo** 🎉 | ~~€99~~ | 300 req/min, AI advisor, 25 providers |
| **Tiny Catfunds** | **€1.90/user/mo** 🎉 | ~~€19~~ | 1k req/min, teams, 3 barks/yr |
| **Enterprise** | **€39.60/user/mo** 🎉 | ~~€396~~ | 10k req/min, on-premise, 15 barks/yr, SSO, SLA |

> 🚧 **90% development discount** — valid until May 2027. Prices shown are after discount. We're still in development, and the cat wants you to build with us.

Yearly = 2 months free. `billing upgrade pro` to start.

---

## 5. Running Locally (Devs)

```bash
# Clone
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd cat-finance-analytics-shell-miau

# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# Frontend
cd ../frontend
npm install
npm run dev
# Opens http://localhost:5173

# Full stack (Docker)
docker compose up -d
```

---

## 6. Key Docs

| Doc | What |
|-----|------|
| [COMMANDS.md](COMMANDS.md) | All 160+ terminal commands |
| [API.md](API.md) | REST API reference (515+ endpoints) |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture |
| [SECURITY.md](SECURITY.md) | Security architecture |
| [COMPLIANCE](compliance/README.md) | BaFin/GDPR compliance (12 docs) |
| [DEPLOY.md](DEPLOY.md) | Production deployment |

---

## 7. The Cat's Rules

1. **Read the docs.** The cat wrote them. Disrespect noted.
2. **Log before asking.** `cat your-logs` counts.
3. **Buy tuna.** The cat accepts subscription payments and emotional support.
4. **Don't break the build.** The cat will know.
5. **Have fun.** Finance is serious. The cat is not.

---

*"The cat types faster than you. The cat trades better than you. The cat napped through the 2008 crash and came out ahead. Be more like the cat."*
