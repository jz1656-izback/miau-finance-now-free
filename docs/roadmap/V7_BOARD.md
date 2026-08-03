# 🐱 V7 "Purrtechno Kitten Era" — Party, Learn, Ship

```
   ╱|、
  (˚ˎ 。7     "v6 made it omniscient. v7 makes it *fun*."
   |、˜〵      "kittens, beats, neon, rave, AGI, tuna."
   じしˍ,)ノ    "the cat hired interns. the interns took over."
```

---

## Sprint Goal

Transform Miau Finance from a professional trading terminal into a **neon-lit kitten nightclub where finance meets party**. Onboard users with 10 fintech kitten characters. Make the terminal pulse. Let kittens trade. Ship the rave.

---

## Task Board

### 🎓 V7-001: Kitten Intern Program
*Gamified onboarding — 10 kittens, each teaching a real fintech skill*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-001a | Design kitten character system — name, role, emoji, color per kitten | design-dev | `frontend/src/data/kittens.ts` | 2h |
| V7-001b | Build `/kittens` terminal command — list squad, show progress | frontend-dev | `frontend/src/lib/commands.ts` | 2h |
| V7-001c | Skill tree backend — kitten unlocks, progress tracking | backend-dev | `backend/app/services/kittens.py` | 3h |
| V7-001d | Kitten skill tree API endpoints | backend-dev | `backend/app/api/kittens.py` | 2h |
| V7-001e | Kitten onboarding UI — progress dashboard | frontend-dev | `frontend/src/components/KittenDashboard.tsx` | 4h |
| V7-001f | Education platform kitten integration — courses per kitten | docs-dev | `education-platform/src/courses/kittens/` | 4h |
| V7-001g | "Kitten Squad Commander" badge + achievement system | frontend-dev | `frontend/src/lib/achievements.ts` | 2h |
| V7-001h | Kitten tests + docs | test-dev + docs-dev | `backend/tests/`, `docs/KITTENS.md` | 3h |

### 🤖 V7-002: Kitten AI Advisor Personalities
*10 AI personalities, each with a distinct strategy and vibe*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-002a | AI personality system — persona prompt templates per kitten | ai-dev | `backend/app/services/ai/personalities.py` | 3h |
| V7-002b | `/ask <kitten> "<question>"` terminal command | frontend-dev | `frontend/src/lib/commands.ts` | 2h |
| V7-002c | `/ask squad "<question>"` — parallel debate mode | frontend-dev | `frontend/src/lib/commands.ts` | 3h |
| V7-002d | Personality API endpoint — `POST /api/v1/ai/ask` with persona param | backend-dev | `backend/app/api/ai_commands.py` | 2h |
| V7-002e | Kitten debate UI — multi-column chat view | frontend-dev | `frontend/src/components/KittenDebate.tsx` | 4h |
| V7-002f | Risk profile per personality (conservative→degen) | ai-dev | `backend/app/services/ai/personalities.py` | 2h |
| V7-002g | Personality tests + docs | test-dev + docs-dev | `backend/tests/`, `docs/KITTEN_AI.md` | 3h |

### 🪩 V7-003: Rave Mode — Purrtechno UI
*Terminal theme with color cycling, glowsticks, and party feels*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-003a | CSS keyframe animations — hue-rotate cycling, pulse effects | design-dev | `frontend/src/index.css` | 1h |
| V7-003b | `/rave` command — toggle rave mode with animated background | frontend-dev | `frontend/src/lib/commands.ts` | 1h |
| V7-003c | `/rave --kittens` — dancing kitten animation in terminal | frontend-dev | `frontend/src/components/Terminal.tsx` | 2h |
| V7-003d | Rave cursor — glowstick-style animated cursor | frontend-dev | `frontend/src/index.css` | 1h |
| V7-003e | Party emoji rain — floating emojis in rave mode | frontend-dev | `frontend/src/components/RaveOverlay.tsx` | 2h |
| V7-003f | Color theme presets (neon, cyberpunk, cotton-candy, classic) | design-dev | `frontend/src/themes/` | 2h |
| V7-003g | Rave mode persistence — localStorage remember setting | frontend-dev | `frontend/src/lib/rave.ts` | 30m |

### 🏁 V7-004: Gamified Portfolio — Kitten Racing
*Your portfolio is a litter of kittens on a racetrack*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-004a | Kitten race engine — position → speed, P&L → animation | frontend-dev | `frontend/src/components/KittenRace.tsx` | 3h |
| V7-004b | `/race` terminal command — opens kitten race view | frontend-dev | `frontend/src/lib/commands.ts` | 1h |
| V7-004c | Real-time price feed for race via WebSocket | backend-dev | `backend/app/api/ws/race.py` | 3h |
| V7-004d | Kitten customization — hat, color, size per holding | frontend-dev | `frontend/src/components/KittenRace.tsx` | 2h |
| V7-004e | Race track UI — lanes, finish line, leaderboard | design-dev | `frontend/src/components/RaceTrack.tsx` | 3h |
| V7-004f | Race tests + docs | test-dev + docs-dev | `frontend/tests/`, `docs/RACE.md` | 2h |

### 🎨 V7-005: Neon Market Visualizer
*Globe + charts with bloom, glow, confetti*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-005a | Three.js post-processing bloom effect on MiauGlobe | frontend-dev | `frontend/src/components/MiauGlobe.tsx` | 3h |
| V7-005b | Stock glow intensity = volatility (brighter = more volatile) | frontend-dev | `frontend/src/components/MiauGlobe.tsx` | 2h |
| V7-005c | Confetti particle system for portfolio green days | frontend-dev | `frontend/src/components/ConfettiOverlay.tsx` | 2h |
| V7-005d | Neon color palette for market layers | design-dev | `frontend/src/themes/neon.ts` | 1h |
| V7-005e | Ticker marquee — scrolling stock ticker in terminal header | frontend-dev | `frontend/src/components/TickerMarquee.tsx` | 2h |

### 🔊 V7-006: Purrtechno Sound Pack
*WebAudio synthesis — purrs, beats, airhorns*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-006a | WebAudio synth engine — OscillatorNode for cat sounds | frontend-dev | `frontend/src/lib/sound.ts` | 2h |
| V7-006b | Market event sounds — purr (up), meow (down), airhorn (trade) | frontend-dev | `frontend/src/lib/sound.ts` | 2h |
| V7-006c | `/sound` command — toggle audio on/off + volume | frontend-dev | `frontend/src/lib/commands.ts` | 1h |
| V7-006d | Sound pack presets (purrtechno, classical, office-safe) | frontend-dev | `frontend/src/lib/sound.ts` | 2h |

### 📰 V7-007: Purrtechno Times
*Daily rhyming market news from a cat news anchor*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-007a | Rhyming market recap generator — template + batch-prices data | ai-dev | `backend/app/services/ai/miau_news.py` | 2h |
| V7-007b | `/miau-news` terminal command | frontend-dev | `frontend/src/lib/commands.ts` | 1h |
| V7-007c | Cat news anchor ASCII art (varies by market direction) | design-dev | `frontend/src/data/miau_news_art.ts` | 1h |
| V7-007d | News API endpoint — `GET /api/v1/miau-news` | backend-dev | `backend/app/api/fun.py` | 1h |

### 😼 V7-008: Catnip Market
*Internal meme economy — teach crypto risk through catnip*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-008a | Catnip price engine — random walk with volatility | backend-dev | `backend/app/services/fun/catnip.py` | 1h |
| V7-008b | `/catnip` — price, buy, sell, portfolio commands | frontend-dev | `frontend/src/lib/commands.ts` | 2h |
| V7-008c | Catnip chart — sparkline in terminal | frontend-dev | `frontend/src/lib/commands.ts` | 1h |
| V7-008d | 10% daily "rug pull" — teaches crypto risk | backend-dev | `backend/app/services/fun/catnip.py` | 30m |
| V7-008e | Catnip leaderboard — who has the most imaginary catnip wealth | frontend-dev | `frontend/src/lib/commands.ts` | 1h |

### 🤖 V7-009: AGI Kitten Trading Desk (Phase 19 + 20)
*Autonomous trading by AI kitten agents — the endgame*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-009a | Multi-strategy ensemble (each kitten = one strategy) | backend-dev | `backend/app/services/hedgefund/strategies.py` | 6h |
| V7-009b | Kitten trade log — kittens write to AGENT_LOG.md | backend-dev | `backend/app/services/hedgefund/kitten_log.py` | 2h |
| V7-009c | `/desk` command — kitten trading desk terminal | frontend-dev | `frontend/src/lib/commands.ts` | 3h |
| V7-009d | Guardian mode — human veto, risk limits, oversight | backend-dev | `backend/app/services/hedgefund/guardian.py` | 4h |
| V7-009e | Tuna-based P&L attribution — kittens earn tuna on profits | backend-dev | `backend/app/services/hedgefund/tuna.py` | 2h |
| V7-009f | Kitten leaderboard — top performer gets featured | frontend-dev | `frontend/src/components/KittenLeaderboard.tsx` | 2h |
| V7-009g | Full Phase 19 hedgefund backend | backend-dev | `backend/app/services/hedgefund/` | 20h |
| V7-009h | Full Phase 20 DAO integration | backend-dev | `backend/app/services/dao/` | 20h |

### 🧪 V7-010: Testing
*Because kittens need quality assurance too*

| ID | Task | Agent | File | Est. |
|----|------|-------|------|------|
| V7-010a | Kitten API tests | test-dev | `backend/tests/test_api/test_kittens.py` | 3h |
| V7-010b | Kitten AI personality tests | test-dev | `backend/tests/test_api/test_kitten_ai.py` | 3h |
| V7-010c | Kitten race component tests | test-dev | `frontend/tests/race.test.ts` | 2h |
| V7-010d | Rave mode render tests | test-dev | `frontend/tests/rave.test.ts` | 2h |
| V7-010e | Catnip market tests | test-dev | `backend/tests/test_api/test_catnip.py` | 2h |

---

## Summary

| Epic | Theme | Tasks | Est. Time |
|------|-------|-------|-----------|
| **V7-001** | Kitten Intern Program | 8 | 22h |
| **V7-002** | Kitten AI Advisor | 7 | 19h |
| **V7-003** | Rave Mode UI | 7 | 9.5h |
| **V7-004** | Kitten Racing | 6 | 14h |
| **V7-005** | Neon Market Visualizer | 5 | 10h |
| **V7-006** | Sound Pack | 4 | 7h |
| **V7-007** | Purrtechno Times | 4 | 5h |
| **V7-008** | Catnip Market | 5 | 5.5h |
| **V7-009** | AGI Kitten Trading Desk | 8 | 59h |
| **V7-010** | Testing | 5 | 12h |
| **Total** | | **59** | **~163h** |

```
   ╱|、
  (˚ˎ 。7     "v7 is the party. v8 is the hangover."
   |、˜〵      "ship the kittens. drop the beats. hire the interns."
   じしˍ,)ノ    "the catnip visions are now sprint tickets."
```
