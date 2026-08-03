# 🐱 FIX LOG — Miau Finance Bug Squashing

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "Every bug squashed is a catnap earned."
```

> "Code reviews are like bath time for cats: nobody wants them, but they prevent disasters."

---

## Q-9: API Retry Logic (LOW)
- Added exponential backoff + jitter to `fetchJSON` in `frontend/src/lib/api.ts`
- Retries network errors (`TypeError`) and 5xx server errors up to 3 times
- Skips 4xx client errors (no retry)
- Backoff: `1s → 2s → 4s` + random ±500ms jitter, capped at 10s

## Q-8: SQL Injection Pattern → ORM Refactor (MEDIUM)
- Created `backend/app/models/__init__.py` with SQLAlchemy ORM models:
  - `Instrument` (25 columns, 2 relationships, 3 indices)
  - `MarketData` (13 columns, FK, unique constraint, 2 indices)
- Refactored `backend/app/api/instruments.py` — all 5 endpoints now use ORM `select()` instead of `text(f"...")`
- Eliminates raw SQL concatenation pattern entirely

## P6.5-1: JWT Auth Frontend (CRITICAL)
- Created `frontend/src/lib/auth.ts` — centralized auth module:
  - `getToken()` / `setToken()` / `clearToken()` / `isAuthenticated()`
  - `authHeaders(extra?)` — returns `{ Authorization: 'Bearer ...' }`
  - `login(username, password)` — calls `POST /api/v1/auth/token`
  - `logout()` / `authFetch()` wrappers
- Wired into `api.ts` `fetchJSON`: auto-attaches `Authorization` header, auto-clears on 401
- Refactored `commands.ts`: removed 11 inline `localStorage.getItem('token')` → `authHeaders()`
- Added `login` and `logout` terminal commands
- Updated HELP text

## P6.5-10: React Error Boundary + Offline Handling (MEDIUM)
- Created `frontend/src/components/ErrorBoundary.tsx` — catches React errors with cat-themed fallback UI (😿 error screen + retry button)
- Created `frontend/src/components/OfflineHandler.tsx` — detects `online`/`offline` events, shows red banner when offline
- Wired both into `App.tsx` wrapping the entire app

## TypeScript Fixes in Terminal.tsx
- Restored `clock` state (was removed by another agent, breaking compilation)
- Updated health check `useEffect` to be self-contained (uses `fetch` but no `setConnected`)
- Removed orphaned `ConnectionDot` JSX + unused `connected`/`setConnected` state (leftover from partial cleanup)

## P6.5-13: Fix Middleware Issues (MEDIUM)
- **AuditLoggingMiddleware** (CRITICAL BUG FIX):
  - Was calling `await request.body()` before `call_next`, which consumed the request stream
  - This **broke all POST/PUT/PATCH endpoints** — the route handler would receive an empty body
  - Fix: Moved `call_next` before body reading, removed body from audit log to avoid stream consumption
- **InputSanitizationMiddleware** (NO-OP → IMPLEMENTED):
  - Was a no-op: `dispatch()` just called `call_next()` and returned without any sanitization
  - Was not even registered in `main.py`
  - Fix: Implemented XSS/SQLi blocking via regex patterns on query strings, path, and parameter values
  - Blocks: `<script`, `javascript:`, `onerror=`, `SELECT.*FROM`, `DROP TABLE`, shell injection chars
  - Registered in `main.py` as first middleware (defense-in-depth layer)
- **Pagination**: Already correctly implemented with `limit`/`offset` query params and validation on all list endpoints

## P6.5-9: TypeScript Type Safety Overhaul (MEDIUM)
- Enabled `noUnusedLocals: true`, `noUnusedParameters: true`, `noImplicitReturns: true` in `tsconfig.json`
- Fixed 22 errors across 11 files:
  - `CatScorecard.tsx` — removed unused `React`, `TrendingUp`, `Heart`, `Zap` imports; fixed useEffect return path
  - `Terminal.tsx` — removed unused `hideMapControls` param
  - `WorldMap.tsx` — removed unused `lerpColor` function
  - `commands.ts` — fixed unused destructured var in `.map()`
  - `Dashboard.tsx` — removed unused `BarChart`, `Bar` imports
  - `InstrumentView.tsx` — removed unused `TrendingUp`, `TrendingDown` imports
  - `MapView.tsx` — removed unused `useEffect` import
  - `ObjectBrowser.tsx` — removed unused `Filter`, `Plus` imports
  - `PortfolioView.tsx` — removed unused `TrendingUp`, `TrendingDown` imports
  - `SearchResults.tsx` — removed unused `ArrowLeft` import
  - `TradeView.tsx` — removed unused `Filter` import

---

```
  ╱|、
 (˚ˎ 。7  
  |、˜〵          
 じしˍ,)ノ    "Bugs squashed: 18. Catnaps taken: 47.
               A fair trade in any developer's book. 🐱"
```
