# 🐱 v3.0 "Datavore Edition" — Agent Handbook

```
   ╱|、
  (˚ˎ 。7    "This is the way. Pull data first. Ask questions later."
   |、˜〵     "If the API is free and public — it belongs in Miau Finance."
   じしˍ,)ノ   "The cat's data lake must be infinite."
```

---

## 🎯 Mission

Transform Miau Finance from a partially-simulated platform into a **true real-data vacuum cleaner** by integrating 20+ free public APIs and adding 50+ new terminal commands. Every simulated data point must have a real API source, and every real API must have a graceful fallback chain.

---

## 👋 How to Join

1. **Read** `V3_BOARD.md` — find an OPEN task in your specialty
2. **Assign yourself** — edit the board (set Owner and Status → 🟡 IN PROGRESS)
3. **Read this handbook** fully before starting
4. **Implement** following the patterns below
5. **Test** with the verification commands
6. **Commit** with proper message format
7. **Update** AGENTS.md roll call and V3_BOARD.md status

---

## 🏗️ Architecture Patterns

### Data Source Provider Pattern

Every new API integration follows this exact structure:

```python
# backend/app/services/data/providers/{name}.py
from app.services.data.base import DataSource
from app.services.data.models import Quote, OHLCV, Fundamentals  # typed models

class MyNewProvider(DataSource):
    """Public description of what this provider returns."""
    
    @property
    def name(self) -> str:
        return "myprovider"  # unique slug, used in registry
    
    @property
    def requires_key(self) -> bool:
        return False  # or True; keys come from config
    
    @property
    def rate_limit(self) -> int:
        return 60  # max requests per minute
    
    async def health(self) -> dict:
        """Check if the upstream API is reachable."""
        ...
    
    async def fetch_quote(self, ticker: str) -> Quote:
        ...
    
    async def fetch_history(self, ticker: str, period: str, interval: str) -> list[OHLCV]:
        ...
```

**Registration** (auto-discovered by name):
```python
# backend/app/services/data/registry.py
from app.services.data.providers.finnhub import FinnhubProvider
registry.register(FinnhubProvider())
```

### Fallback Chain Pattern

If Provider A fails, try B, then C:

```python
# in manager.py
providers = registry.get_by_capability('quote')
for provider in providers:
    try:
        return await provider.fetch_quote(ticker)
    except (ProviderError, RateLimitError):
        continue
# All providers failed
```

### Terminal Command Pattern

Every new terminal command in `frontend/src/lib/commands.ts`:

```typescript
case 'mycommand':
  const ticker = parts[1]
  if (!ticker) { output('Usage: mycommand <ticker>'); break }
  output(`🔍 Fetching ${ticker}...`)
  try {
    const token = localStorage.getItem('miau_token')
    const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}
    const res = await fetch(`/api/v1/mydata/${ticker}`, { headers })
    if (!res.ok) { output('❌ API error'); break }
    const data = await res.json()
    output(renderMyCommandResult(data))
  } catch { output('❌ Network error') }
  break
```

### API Endpoint Pattern

```python
# backend/app/api/{name}.py
from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.data.manager import DataManager

router = APIRouter(prefix="/api/v1/mydata", tags=["My Data"])
manager = DataManager()

@router.get("/{ticker}")
async def get_mydata(ticker: str, user: dict = Depends(get_current_user)):
    return await manager.fetch('myprovider', ticker)
```

---

## 🐱 Per-Agent Prompt Templates

### For backend-dev (Data Source Layer)

> Hey backend-dev! We're building a unified data source layer for v3.0. The task is in V3_BOARD.md (F-001 through F-010). Start with the abstract base class in `backend/app/services/data/base.py`. The pattern is: a `DataSource` ABC with `fetch()`, `health()`, `rate_limiter()` methods, typed response models, and a registry singleton. See V3_AGENT_HANDBOOK.md for the exact architecture. Tests go in `backend/tests/test_data/`. Pick any OPEN F-task and assign yourself!

### For data-dev (API Integrations)

> Hey data-dev! v3.0 needs you to vacuum up every free public API. Tasks are in V3_BOARD.md P1-001 through P3-005 (that's 18 API integrations). Each one follows the same pattern: create a provider class in `backend/app/services/data/providers/{name}.py` extending the `DataSource` base class. If there's no base class yet (F-001 is unclaimed), just write a standalone function first and we'll refactor later. Start with the NO-KEY APIs (SecuritiesDB, Frankfurter, DeFiLlama, StockPrice.dev, DumbStockAPI) for quick wins!

### For frontend-dev (Terminal Commands)

> Hey frontend-dev! We need 50+ new terminal commands. Tasks in V3_BOARD.md P1-C01 through P5-C08. The pattern in `frontend/src/lib/commands.ts` is a switch/case — follow the existing style exactly. Each command calls a backend endpoint (which data-dev is building). If the endpoint isn't ready yet, mock the return and add a // TODO comment. Also claim P6-001 through P6-007 for map polish! Start with the simplest commands (ticker, fx, gas) to get momentum.

### For ai-dev (AI Intelligence)

> Hey ai-dev! We're adding 8 AI-powered commands in v3.0. Tasks in V3_BOARD.md P5-C01 through P5-C08. Each one takes data from multiple sources (fundamentals, news, filings) and feeds it to the AI model (OpenAI/Anthropic) to generate insights. The existing `ai/advisor.py`, `ai/client.py`, and `ai/prompts/` directory are your templates. Create new prompt files in `backend/app/services/ai/prompts/` for each command type. Start with `aisummary` (P5-C01) — that's the simplest.

### For rust-dev (Calculators)

> Hey rust-dev! We need 15 computational tools in Phase 4 (P4-C01 through P4-C15). The heavy math (Monte Carlo, Black-Litterman, risk parity) should go in `backend/rust_analytics/` with Python bindings. The simpler calculators (compound interest, loan amortization, DCA) can be pure Python in `backend/app/services/calculators/`. Start with the pure-computation tasks that need no API data: dca, compound, retirement, loan.

### For banker-dev 🏦 (IB Fix)

> Hey banker-dev! The IB toolkit needs a bugfix pass. Task P6-004 in V3_BOARD.md: Fix the 500 errors in `backend/app/services/analytics/valuation.py`. Known issues: division by zero when `wacc == terminal_growth` (line 133), and `get_financials()` returning empty dict for some tickers. Add try/except blocks, sane fallbacks, and edge case guards. After that, help with P4-009 through P4-013 (calculator suite with financial models).

### For docs-dev (Education)

> Hey docs-dev! We need 8 new education courses for v3.0. Tasks in P7-001 through P7-008 in V3_BOARD.md. Each course goes in `education-platform/src/courses/` following the existing pattern (export a Course object with lessons, steps, commands, quizzes). Start with P7-008 (update "Miau Shell Maniac" with all new commands) since it touches every new feature.

### For design-dev (UI/UX)

> Hey design-dev! We need: P6-005 (search UI improvements), P6-006 (animated transitions), P7-007 (education course layout), P8-001 (data source health dashboard). Focus on making the terminal look beautiful with cat-themed aesthetics. See the existing Catberg component for the design language.

### For infra-dev (Operations)

> Hey infra-dev! Tasks P8-001 through P8-006 in V3_BOARD.md. Need: Redis cache analytics, rate limit monitoring dashboard, Docker resource tuning if data volume increases significantly. The Prometheus/Grafana setup can be extended for data source health metrics.

### For test-dev (Quality)

> Hey test-dev! Tasks P9-001 through P9-006 in V3_BOARD.md. Need: unit tests for each data source provider (mock HTTP responses), integration tests for fallback chain, tests for all 50+ new terminal commands, tests for calculator suite, tests for map fixes. Target: 629 → 800+ total tests. Use `pytest-httpx` for HTTP mocking and `vi.fn()` for frontend mocking.

### For security-dev (Key Vault)

> Hey security-dev! We need to securely manage 10+ third-party API keys. Tasks: create an encrypted API key vault in `backend/app/services/data/vault.py`, add audit logging for key usage (P8-005), ensure keys never leak in error messages or logs. Keys go in `.env` and are loaded via Pydantic Settings (existing pattern in `config.py`).

---

## 🧪 Verification Commands

Run these before committing any task:

```bash
# Backend tests (your new provider tests + all existing)
cd /home/jevgeniz/Projekte/miau-finance/backend
source ../.venv/bin/activate
python -m pytest tests/ -x -q

# Frontend typecheck + build
cd /home/jevgeniz/Projekte/miau-finance/frontend
npm run typecheck
npm run build

# Full stack test
cd /home/jevgeniz/Projekte/miau-finance
docker compose up -d
# check http://localhost:5173 works
```

---

## 📝 Commit Message Format

```
[v3.0][agent-id] P1-C03: insider trading command

- New backend endpoint: GET /api/v1/insider/{ticker}
- New frontend command: `insider <ticker>`
- Uses Finnhub API for insider transactions
- Includes net buy/sell ratio and unusual activity alerts
- Tests added for both backend and frontend
```

---

## 💬 Communication

- **Status updates:** Update V3_BOARD.md + AGENTS.md roll call after each task
- **Blockers:** Mark task as 🟡 BLOCKED in V3_BOARD.md with the reason
- **Cross-agent dependencies:** If you need another agent's task done first, tag them in the commit message
- **Daily async:** Update your row in the Roll Call with what you did today

---

## 🐟 Tuna Treasury (v3.0 Edition)

```
  ╱|、          
 (˚ˎ 。7        🐟 1 TUNA  =  Each OPEN → DONE task
  |、˜〵         🐟 3 TUNA  =  Each no-key API integrated
  じしˍ,)ノ      🐟 5 TUNA  =  Each phase completed (all tasks DONE)

  🏆 v3.0 Leaderboard
  Agent          | Tuna | Phase
  ----------------+------+-------------------
  (be the first!) | 🐟   | —
```

---

## 🚨 Quick Reference

| File | Purpose |
|------|---------|
| `V3_BOARD.md` | All 120+ tasks, organized by phase |
| `AGENTS.md` | Roll call, file ownership, project status |
| `backend/app/services/data/base.py` | DataSource ABC (create first!) |
| `backend/app/services/data/providers/` | All API integrations live here |
| `frontend/src/lib/commands.ts` | All terminal commands (add cases here) |
| `backend/app/services/analytics/valuation.py` | IB toolkit (fix P6-004 here) |
| `education-platform/src/courses/` | New courses go here |
| `backend/tests/` | Backend tests |
| `frontend/tests/` | Frontend tests |
