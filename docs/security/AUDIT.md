# 🐱 Miau Finance — Code Audit Report

> **Date:** 2026-05-20  
> **Scope:** Full codebase audit (frontend + backend + infra)  
> **Total issues found:** 72

---

## 🔴 CRITICAL (Must fix — app crash or data loss)

### C-01: Duplicate API Routes — App Won't Start
**File:** `backend/app/api/datavore.py` lines 1388 & 1585, 1406 & 1591  
**Issue:** Two `@router.get("/insider/{ticker}")` and two `@router.get("/short/{ticker}")` definitions. FastAPI raises `AssertionError: Duplicate route` on startup.  
**Fix:** Remove the duplicate routes (lines 1585 and 1591).

### C-02: Non-Existent Provider Methods Called
**File:** `backend/app/api/datavore.py` lines 1379, 1382  
**Issue:** `await finnhub.screener(**params)` and `await securitiesdb.screener(limit)` — neither provider has a `screener()` method. `AttributeError` at runtime.  
**Fix:** Implement `screener()` on both providers or remove the route.

### C-03: ImportError — `ConfigError` Doesn't Exist
**Files:** `eia.py` line 36, `imf.py` line 35, `fred.py` line 46, `hfdata.py` line 36, `mobula.py` line 34  
**Issue:** All import `from app.services.data.base import ConfigError` — but `ConfigError` is not defined in `base.py`. Only `DataSourceError`, `RateLimitError`, `ProviderUnavailableError` exist. `ImportError` at startup.  
**Fix:** Replace `ConfigError` with `DataSourceError` or define it in `base.py`.

### C-04: CSRF Middleware Blocks All SPA Write Operations
**File:** `backend/app/middleware/csrf.py`, wired in `main.py` line 181  
**Issue:** CSRF middleware checks for `X-CSRF-Token` header on all non-safe methods. The frontend SPA never sends this header (no evidence of reading `csrf_token` cookie and reflecting it). All POST/PUT/DELETE return 403.  
**Fix:** Either whitelist all API paths in the CSRF middleware, or implement proper CSRF token handling in the frontend.

### C-05: Module-Level Side Effects Crash Startup
**File:** `backend/app/main.py` lines 139–144  
**Issue:** `init_notification_service()` and `start_scheduler()` run at **module import time**, not inside the startup event handler. They may depend on async resources (Redis, DB) that aren't ready.  
**Fix:** Move both calls inside `@app.on_event("startup")`.

### C-06: MarkerCluster Crash on Company Click
**File:** `frontend/src/components/WorldMap.tsx` lines 356–358  
**Issue:** `map.removeLayer(oldCluster)` during a MarkerCluster spiderfiy animation causes `Cannot read properties of undefined (reading '_zoom')`. This is the intermittent browser crash.  
**Fix:** Cancel spider animations before removal, or guard with `oldCluster.unspiderfy()`.

### C-07: Duplicate Case Statements — Dead Code
**File:** `frontend/src/lib/commands.ts`  
**Issue:** 11 command cases appear twice (`correlation`, `apikey`, `insider`, `short`, `profile`, `ticker`, `stablecoins`, `dexs`, `fees`, `famanch`, `passiveflow`). The second instance is dead code — never reached.  
**Fix:** Remove all duplicate case statements (lines 1729, 3637, 4346, 4365, 4393, 4412, 4470, 4483, 4497, 4535, 4572).

### C-08: `calc pnl` Unreachable
**File:** `frontend/src/lib/commands.ts` line 2302  
**Issue:** `case 'calc pnl':` is a multi-word string but the command parser uses `parts[0]` as the command key. `calc pnl` becomes `command = 'calc'` — never matches.  
**Fix:** Handle two-word commands by checking `parts[0] + ' ' + parts[1]` before the main switch, or change to `case 'calc':` with a `pnl` subcommand.

### C-09: Bare Ticker Lookup Broken
**File:** `frontend/src/lib/commands.ts` lines 447, 4830  
**Issue:** `command` is lowercased to `'aapl'`, but the regex `/^[A-Z]{1,5}$/` requires uppercase. All bare ticker lookups silently fail.  
**Fix:** Change regex to `/^[A-Za-z]{1,5}$/` or uppercase `command` instead.

---

## 🟠 HIGH (Major functionality issue)

### H-01: 30+ Unhandled Promise Rejections
**File:** `frontend/src/lib/commands.ts` — 30+ locations  
**Issue:** `.then(r => r.json())` without `.catch()` — network errors become unhandled promise rejections that may crash the Node process (and in browser, flood the console).  
**Fix:** Add `.catch(() => {})` or convert to `await safeJson(res, addLine)` pattern used elsewhere.

### H-02: Return Type Mismatch — `fetch_fundamentals` Returns Dict, Not Model
**File:** `backend/app/services/data/providers/yahoo.py` lines 59–63  
**Issue:** Declared to return `Fundamentals` (pydantic model) but returns a plain dict. Callers accessing `.model_dump()` or typed fields will get `AttributeError`.  
**Fix:** Return a `Fundamentals` model instance, or update the type hint.

### H-03: Massive Overlay Rebuild on Every Toggle
**File:** `frontend/src/components/WorldMap.tsx` lines 414–640  
**Issue:** The overlays effect has 11 dependencies. Toggling `showHairballs` destroys and recreates ALL overlays (boats, jets, cats, ISS, commodities, bonds, DeFi). Extremely wasteful.  
**Fix:** Split into separate effects per overlay type.

### H-04: Boat Animation Broken — Index Mismatch
**File:** `frontend/src/components/WorldMap.tsx` lines 468, 606–607  
**Issue:** Only 1 marker pushed per boat route, but the animation loop reads 2 (`ol.boats[i*2]` and `ol.boats[i*2+1]`). Indices 19+ are `undefined` — most boats never animate.  
**Fix:** Push 2 markers per route (like the jet code does at line 488).

### H-05: Full Data Refetch on Every Zoom/Drag
**File:** `frontend/src/components/WorldMap.tsx` line 786, 838  
**Issue:** Live-data effect depends on `[zoom]`. Every zoom or drag fires `setZoom` → 5+ API calls (prices, commodities, bonds, defi, worldmap). Creates a storm of fetches.  
**Fix:** Debounce zoom changes or remove `zoom` from live-data effect deps.

### H-06: `_getKey()` Methods Are `async` But Synchronous
**Files:** `eia.py`, `imf.py`, `fred.py`, `hfdata.py`, `mobula.py`  
**Issue:** Methods declared `async` just read `environ.get()` — synchronous. Misleading and adds unnecessary microtask overhead.  
**Fix:** Make them sync properties.

### H-07: `sectors_exposure` / `sectorsexposure` Name Mismatch
**File:** `frontend/src/lib/commands.ts` lines 140 (help) vs 1758 (case)  
**Issue:** Help documents `sectors_exposure` but the case is `sectorsexposure`. Users following help get "command not found".  
**Fix:** Add `case 'sectors_exposure':` that falls through to the existing case.

### H-08: Chaos Trigger Is Dead Code
**File:** `frontend/src/lib/commands.ts` lines ~4063–4078  
**Issue:** A bare `{ ... }` block with no case label sits between `case 'achievements':` (which `break`s) and `case 'esg':`. Completely unreachable.  
**Fix:** Move the chaos trigger to the end of `executeCommand()`, outside the switch.

### H-09: Missing `try/catch` on Provider Calls
**File:** `backend/app/api/datavore.py` — 30+ routes  
**Issue:** Most routes call provider methods without `try/catch`. Provider exceptions become 500 errors instead of graceful error responses.  
**Fix:** Wrap provider calls in `try/except` and return appropriate HTTP error codes.

---

## 🟡 MEDIUM (Functionality degraded)

### M-01: Unbounded In-Memory Cache Growth
**File:** `backend/app/services/data/cache.py` line 28  
**Issue:** In-memory cache `self._memory` has no size limit or eviction policy. Grows unboundedly → OOM.  
**Fix:** Add LRU eviction or max size limit.

### M-02: `"undefinedx"` Displayed When IB Data Missing
**File:** `frontend/src/components/WorldMap.tsx` line 1225  
**Issue:** `ibData.lbo.moic?.toFixed(2) + 'x' || '—'` — when `moic` is `undefined`, `undefined?.toFixed(2)` → `undefined`, `undefined + 'x'` → `"undefinedx"` (truthy), so `|| '—'` never triggers.  
**Fix:** `{ibData.lbo.moic != null ? ibData.lbo.moic.toFixed(2) + 'x' : '—'}`

### M-03: Stale `zoom` Closure in Data Fetch
**File:** `frontend/src/components/WorldMap.tsx` line 742  
**Issue:** The data-fetch success callback captures `zoom` from when the effect first ran (default 3). If user zooms before fetch completes, initial slice is wrong.  
**Fix:** Read `zoom` from ref instead of closure, or re-slice after fetch.

### M-04: `clusterVersionRef` Prevents Price Color Updates
**File:** `frontend/src/components/WorldMap.tsx` line 343  
**Issue:** When only prices change (same `companies.length`), `clusterVersionRef` prevents rebuild. Marker colors stay stale.  
**Fix:** Include a price-change checksum in the version computation.

### M-05: Missing `key` Props on Fragments
**File:** `frontend/src/components/WorldMap.tsx` lines 1082, 1100, 1114  
**Issue:** `<></>` fragments inside `.map()` loops lack `key` props. React falls back to index-based reconciliation.  
**Fix:** Add `key` to each fragment.

### M-06: WebSocket Proxy Not Configured
**File:** `frontend/vite.config.ts`  
**Issue:** Vite proxy has `changeOrigin: true` but no `ws: true`. WebSocket connections to `/api/v1/ws/` won't be proxied.  
**Fix:** Add `ws: true` to proxy config.

### M-07: CDN Scripts/Links Not Cleaned Up
**File:** `frontend/src/components/WorldMap.tsx` lines 258–281  
**Issue:** Leaflet/MarkerCluster CSS and JS appended to `<head>` but never removed on unmount. Duplicate appends if component remounts.  
**Fix:** Remove elements in the cleanup function.

### M-08: Empty `catch {}` Swallows All Errors
**File:** `frontend/src/components/WorldMap.tsx` — 19 locations  
**Issue:** All `.catch(() => {})` silently discard errors. Network failures, JSON parse errors, runtime errors are invisible.  
**Fix:** Add `console.error` at minimum, or better error handling.

### M-09: Chaotic Mode Function Not Accessible
**File:** `frontend/src/lib/commands.ts`  
**Issue:** `chaos` toggle is documented in help but the chaos effects are in a dead-code block (see H-08).  
**Fix:** Move chaos trigger to executeCommand() post-switch.

### M-10: `ConfigError` Import — 5 Providers Affected
**File:** Multiple provider files  
**Issue:** Importing `ConfigError` that doesn't exist. These providers will fail at import time.  
**Fix:** Remove the import or define the exception.

### M-11: HTTP 404 vs 503 Misuse
**File:** `backend/app/api/datavore.py` — multiple routes  
**Issue:** Routes raise `HTTPException(404, "Finnhub not configured")` — 404 means Not Found, but the real issue is Service Unavailable (503) or Configuration Error (500).  
**Fix:** Use appropriate HTTP status codes.

---

## 🟢 LOW (Minor / Cosmetic / Performance)

### L-01: Duplicate Tile-Layer Effects
**File:** `frontend/src/components/WorldMap.tsx` lines 393–411 & 841–852  
**Issue:** Two effects both swap tile layers. Second doesn't handle weather layer. Causes visual flash.

### L-02: rAF Loop Runs When All Animation Is Hidden
**File:** `frontend/src/components/WorldMap.tsx` lines 592–635  
**Issue:** `requestAnimationFrame` runs at 60fps even when boats, jets, and hairballs are all hidden. Minor CPU waste.

### L-03: `data` Reference Change Triggers Full Overlay Rebuild
**File:** `frontend/src/components/WorldMap.tsx` lines 810–820  
**Issue:** Every live-data fetch creates a new `data` object, triggering full overlay destroy+rebuild.

### L-04: `showCompanies` Doesn't Affect Search
**File:** `frontend/src/components/WorldMap.tsx` lines 239, 1282–1292  
**Issue:** Toggling companies off hides markers, but search bar still lists all companies.

### L-05: `generateGlobalCompanies` Sync Block
**File:** `frontend/src/components/WorldMap.tsx` line 727  
**Issue:** 5000-company generator runs synchronously inside a `.then()` callback, blocking the microtask queue.

### L-06: Ticker/Name Array Length Mismatch
**File:** `frontend/src/components/WorldMap.tsx` line 683–684  
**Issue:** `tickers` has 62 entries, `names` has 55. High-index companies get generic names. `LVMH` duplicated in names.

### L-07: All `_getKey()` Methods Async But Sync
**File:** `eia.py`, `imf.py`, `fred.py`, `hfdata.py`, `mobula.py`  
**Issue:** `async def` methods that just return `environ.get()` — misleading API design.

### L-08: Operator Precedence Confusion
**File:** `frontend/src/lib/commands.ts` line 1050  
**Issue:** `(w as number * 100)` parsed as `w as (number * 100)`, not `(w as number) * 100`.

### L-09: Redundant Dynamic Import
**File:** `frontend/src/lib/commands.ts` line 611  
**Issue:** `clearToken` dynamically re-imported from `./auth` even though it's already imported at top of file.

### L-10: Undocumented Commands (14)
**File:** `frontend/src/lib/commands.ts`  
**Issue:** `heatmap`, `scorecard`, `split`, `ontypes`, `onobjects`, `instruments`, `instypes`, `sectorslist`, `anportfolio`, `anrisk`, `optperf`, `newsbatch`, `cryptotop`, `papers` have case handlers but no help text.

### L-11: Dockerfile Redundant COPY
**File:** `frontend/Dockerfile` lines 18–19  
**Issue:** First `COPY` is overwritten by second `COPY --chown`. Remove the first.

### L-12: Frontend Uses Vite Dev Server in Docker
**File:** `docker-compose.yml` line 84  
**Issue:** `target: builder` with `npm run dev` — not production. Vite dev server exposes source maps, HMR, no compression.

### L-13: `version` Attribute Deprecated in docker-compose.yml
**File:** `docker-compose.override.yml`  
**Issue:** The `version` attribute is obsolete in Docker Compose v2. Causes warnings on every command.

### L-14: Template Literal Bug in Dead Code
**File:** `frontend/src/lib/commands.ts` line 4547  
**Issue:** `R²'.padEnd(20)}` — the `.padEnd()` is inside static text, not `${}`. Only affects dead duplicate code.

### L-15: Memory Leak — `allCompaniesRef` Not Cleaned
**File:** `frontend/src/components/WorldMap.tsx` line 643  
**Issue:** 25K+ company objects retained in ref on unmount.

### L-16: Notification Service / Scheduler Run at Import Time
**File:** `backend/app/main.py` lines 139–144  
**Issue:** Side effects at module level. Should be in startup handler.

### L-17: `authFetch` Without Token Refresh
**File:** `frontend/src/lib/commands.ts` lines 10–24  
**Issue:** Local `authFetch` only clears token on 401 — doesn't attempt refresh like the one from `auth.ts`.

---

## 🔧 Quick Fix Batch (Can fix in <30 min)

1. Remove duplicate routes in `datavore.py` (C-01)
2. Remove or guard `screener()` calls in `datavore.py` (C-02)
3. Fix `"undefinedx"` display (M-02)
4. Remove duplicate case statements (C-07)
5. Fix `chaos` dead code (H-08)
6. Fix `sectors_exposure` / `sectorsexposure` mismatch (H-07)
7. Remove redundant Dockerfile COPY (L-11)
8. Fix bare ticker regex (C-09)
9. Remove `ConfigError` imports (C-03 / M-10)
10. Fix `calc pnl` (C-08)
