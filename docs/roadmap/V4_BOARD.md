# 🐱 V4 "The Great Fixing Era" — Delittering the Litterbox ✅ ALL DONE

```
   ╱|、
  (˚ˎ 。7     "v3 gave us infinite data. v4 makes it not suck."
   |、˜〵      "the cat is tired of cleaning up your mess."
   じしˍ,)ノ    "every deleted file is one less place to hide bugs."
```

---

## Sprint Goal

Clean up technical debt, remove dead code, fix all warnings, and tighten the codebase for the next phase of real feature development.

| Metric | Target | Current |
|--------|--------|---------|
| JS bundle size | < 2MB | 2.2MB + Globe.gl |
| GitHub repo size | < 500MB | > 500MB (venv + JSON bloat) |
| TypeScript strict errors | 0 | many |
| useEffect count (WorldMap) | < 8 | 12 |
| Vendored blobs | 0 | 2 (companies.json copies, .venv) |

---

## Task Board

### 🗑️ V4-001: Remove Dead Bloat

| ID | Task | File(s) | Status |
|----|------|---------|--------|
| V4-001a | ✅ DONE | ✅ DONE | Remove duplicate 11.5MB `companies.json` from `src/data/` (only used by old MiauGlobe import — now lazy-fetches) | `frontend/src/data/companies.json` | |
| V4-001b | ✅ DONE | ✅ DONE | Remove `.venv/` and `venv/` from git tracking + add to `.gitignore` | `.gitignore`, `.venv/`, `backend/venv/` | |
| V4-001c | ✅ DONE | ✅ DONE | Remove nested `logviewer/logviewer/` from git history | `backend/app/static/logviewer/logviewer/` | |
| V4-001d | ✅ DONE | ✅ DONE | Remove old `companies.json` from `frontend/public/data/` (7 shard files replace it) | `frontend/public/data/companies.json` | |

### 🧹 V4-002: Consolidate Map Effects

| ID | Task | File(s) | Status |
|----|------|---------|--------|
| V4-002a | ✅ DONE | Merge tile layer + weather overlay into one effect | `WorldMap.tsx` |
| V4-002b | ✅ DONE | Merge resize observer into init effect | (already in init effect) |
| V4-002c | ✅ DONE | Remove empty mount effect | `WorldMap.tsx` |
| V4-002d | ✅ DONE | Remove duplicate tile layer effect (was race condition) | `WorldMap.tsx` |

### 🔧 V4-003: Fix All Warnings

| ID | Task | File(s) | Status |
|----|------|---------|--------|
| V4-003a | ✅ DONE | ✅ DONE | Fix `billing_balances` migration (create missing table) | `alembic/versions/` | |
| V4-003b | ✅ DONE | ✅ DONE | Fix SecuritiesDB no-screener error in screener endpoint | `datavore.py` | |
| V4-003c | ✅ DONE | ✅ DONE | Fix Yahoo provider bare `DataSourceError` (add try/except wrapper) | `yahoo.py` | |
| V4-003d | ✅ DONE | Fix stale version refs in education platform | `education-platform/src/` | |

### 📦 V4-004: Optimize Bundle

| ID | Task | File(s) | Status |
|----|------|---------|--------|
| V4-004a | Remove unused imports from WorldMap.tsx | `WorldMap.tsx` | ✅ DONE — no unused imports found |
| V4-004c | Tree-shake unused Leaflet controls | `WorldMap.tsx` | ✅ DONE — all controls used |
| V4-005b | Make sure `make up` starts all containers cleanly | `Makefile` | ✅ DONE — 9/9 containers healthy |
| V4-005c | ✅ DONE | Update `AGENTS.md` board header | `AGENTS.md` | |
