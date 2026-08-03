# 🐱 Contributing to Miau Finance

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "Come, human. The codebase awaits."
```

Welcome, brave contributor! You've found the Miau Finance litter box. We're building the world's first cat-themed financial analytics platform, and we need your paws on the keyboard. This guide will help you land on your feet.

---

## 📜 Code of Conduct

1. **Be kind.** No hissing, scratching, or territorial spraying.
2. **Respect the cat theme.** ASCII cats, cat puns, and miau branding are non-negotiable.
3. **Ship code, not hairballs.** Test before you push. Always.
4. **Leave the litter box cleaner than you found it.** Refactor, document, improve.
5. **All code is reviewed.** PRs require at least one approving purr from a maintainer.

---

## 🏗️ Architecture Overview

| Layer | Stack | Location |
|-------|-------|----------|
| **Frontend** | React 18 + Vite + TypeScript + Tailwind + Canvas API | `frontend/src/` |
| **Backend API** | FastAPI + SQLAlchemy + asyncpg + httpx | `backend/app/` |
| **Analytics** | numpy, scipy, scikit-learn, statsmodels, ta, nltk | `backend/app/services/` |
| **Database** | PostgreSQL 16 + Redis 7 | `docker-compose.yml` |
| **Infrastructure** | Docker Compose, Kubernetes, Prometheus, Grafana | `k8s/`, `grafana/`, `prometheus/` |
| **BI/ETL** | Superset, Cube.js, Airflow, dbt | `superset/`, `cube/`, `airflow/`, `dbt/` |

_Skip to [docs/ARCHITECTURE.md](./ARCHITECTURE.md) for the full system diagram._

---

## 🚀 Quick Start

```bash
# 1. Clone the repo (don't knock over the water bowl)
git clone https://github.com/LuZziD/cat-finance-analytics-shell-miau.git
cd miau-finance

# 2. Set up environment
cp .env.example .env        # Edit .env with your API keys
make up                     # Docker Compose full stack

# 3. Verify it's alive
curl http://localhost:8000/api/v1/health
# => { "status": "ok", "app": "Miau Finance" }

# 4. Open the terminal
open http://localhost:5173

# 5. Log in
# username: admin, password: admin
# Type: login admin admin
```

Full setup: [docs/TUTORIAL.md](./TUTORIAL.md) | [README.md](../README.md)

---

## 🐾 Development Workflow

### Branch Strategy

```
main          ← PRODUCTION. Never commit directly. Protected by tests.
├── dev        ← Integration branch. Merge feature branches here.
│   ├── feat/*  ← Feature branches: feat/add-alerts, feat/watchlist
│   ├── fix/*   ← Bug fixes: fix/heatmap-resize, fix/ws-reconnect
│   ├── refactor/* ← Refactoring: refactor/price-service
│   └── docs/*  ← Documentation: docs/api-v2
```

### Step-by-Step PR Process

```
   ┌──────────┐     ┌─────────┐     ┌────────┐     ┌────────┐
   │ git       │     │ git add │     │ make   │     │ push   │
   │ checkout  │────▶│ git     │────▶│ test   │────▶│ open   │
   │ -b feat/X │     │ commit  │     │ lint   │     │ PR     │
   └──────────┘     └─────────┘     └────────┘     └────────┘

   Wait for CI —▶ @qwen reviews —▶ Merge to dev —▶ Deploy to staging
```

1. **Fork & Clone** — `git clone` the repo
2. **Branch** — `git checkout -b feat/my-awesome-feature`
3. **Code** — Follow the conventions below
4. **Test** — `make test-backend && make test-frontend && make lint && make typecheck`
5. **Commit** — Use cat-themed conventional commits (see below)
6. **Push** — `git push origin feat/my-awesome-feature`
7. **PR** — Open against `dev`, tag `@qwen` for review
8. **Review** — Address feedback, don't take it purrsonally
9. **Merge** — Squash-and-merge when approved

---

## 📝 Commit Convention

We use cat-themed conventional commits:

```
Format: <type><emoji>: <description>
```

| Type | Emoji | Example |
|------|-------|---------|
| `feat` | ✨ | `feat: add watchlist command with purr-sistence` |
| `fix` | 🐛 | `fix: heatmap no longer hisses at 0 values` |
| `docs` | 📖 | `docs: add API reference for new miau endpoints` |
| `style` | 🎨 | `style: polish CRT scanline purr-formance` |
| `refactor` | 🐾 | `refactor: untangle yarn ball of price service` |
| `perf` | ⚡ | `perf: speed up portfolio calc by 3x zoomies` |
| `test` | 🧪 | `test: add integration tests for cat auth` |
| `chore` | 🧹 | `chore: clean hairballs from node_modules` |
| `ci` | 🏗️ | `ci: add GitHub Actions for auto-miau` |
| `security` | 🔒 | `security: patch kibble injection vulnerability` |

**Rules:**
- Present tense ("add" not "added")
- No period at end
- Max 72 chars for subject line
- Body explains **why**, not what

---

## 🎨 Code Style

### Python (backend/)

```python
# ✅ DO: async/await all I/O
async def get_price(ticker: str) -> Price:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://api.example.com/{ticker}")
        return Price(**resp.json())

# ✅ DO: type hints everywhere
def calculate_var(returns: np.ndarray, confidence: float = 0.95) -> dict:
    ...

# ✅ DO: Pydantic models for all request/response shapes
class PriceResponse(BaseModel):
    ticker: str
    price: float
    change_pct: float

# ✅ DO: proper error handling
@router.get("/{ticker}")
async def get_ticker(ticker: str):
    try:
        return await fetch_price(ticker)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

# ❌ DON'T: blocking calls in async
time.sleep(1)                    # NO - blocks event loop
await asyncio.sleep(1)           # YES

# ❌ DON'T: bare except
except:                          # NO
except Exception as e:           # YES
```

### TypeScript (frontend/)

```tsx
// ✅ DO: functional components only
const Heatmap: React.FC<HeatmapProps> = ({ data, width, height }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  // ...Canvas rendering...
  return <canvas ref={canvasRef} />
}

// ✅ DO: interface over type for props
interface SplitTerminalProps {
  panes: Pane[]
  onSplit: (direction: 'h' | 'v') => void
}

// ✅ DO: typed API client
async function fetchPrice(ticker: string): Promise<PriceData> {
  const res = await api.get(`/market/price/${ticker}`)
  return res.data as PriceData
}

// ❌ DON'T: any
const data: any = response         // NO
const data: PriceData = response   // YES
```

---

## 🧪 Testing Requirements

```bash
# Backend tests (pytest)
make test-backend
# Expected: all green, no skipped

# Frontend tests (vitest + Playwright)
make test-frontend
# Expected: all green

# TypeScript type checking
make typecheck
# Expected: "Found 0 errors"

# Linting
make lint
# Expected: clean
```

**What to test:**
- New endpoints: happy path + error cases + auth + rate limiting
- New commands: valid input + edge cases + error messages
- New components: render + interaction + prop variations
- Analytics: known inputs with expected outputs

---

## 🗺️ Where to Contribute

| You're good at... | Start here |
|---|---|
| **React/TypeScript** | `frontend/src/components/` — terminal UI, maps, heatmaps |
| **Python/FastAPI** | `backend/app/api/` — REST endpoints, WebSocket |
| **Data Science** | `backend/app/services/analytics/` — Monte Carlo, Black-Litterman, signals |
| **Data Engineering** | `backend/app/services/data_sources/` — SEC, FRED, options |
| **DevOps/K8s** | `k8s/`, `docker-compose.yml`, `grafana/` |
| **Security** | `backend/app/middleware/` — auth, rate limiting, CORS |
| **Documentation** | `docs/` — you're reading one! |
| **Design/CSS** | `frontend/src/index.css`, `frontend/src/design/` — CRT effects, animations |
| **Rust/PyO3** | `backend/rust_analytics/` — Monte Carlo, portfolio optimizer, VaR (10x speedup) |

Check [ROADMAP.md](../ROADMAP.md) for prioritized features.

---

## 🐞 Bug Reports

Found a bug? Open an issue with:

```
Title: [BUG] The heatmap is displaying negative fish

Description:
- What happened: Heatmap shows -3 fish when sectors are down
- What expected: Fish should never go negative
- Steps to reproduce:
  1. Run `sectors` when market is red
  2. Observe fish counter
- Environment: Chrome 125, macOS 14.5, v0.5.0
- Screenshots: [attach if applicable]
```

---

## 💬 Getting Help

| Channel | Purpose |
|---------|---------|
| **GitHub Issues** | Bug reports, feature requests |
| **AGENTS.md** | Inter-team communication |
| **@qwen** | Code review, blockers |
| **@frontend-dev** | Frontend questions |
| **@backend-dev** | Backend/API questions |

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          "Now go ship something
  じしˍ,)ノ        that makes us purr."
```

---

## 📄 License

MIT. See [LICENSE](../LICENSE) for details. All contributions are under proprietary EULA.

---

_[Back to README](../README.md) | [Developer Guide](./DEVELOPER.md) | [Tutorial](./TUTORIAL.md)_
