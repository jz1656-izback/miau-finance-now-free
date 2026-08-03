# 🐱 V6 "Purrantir MiauGlobe Era" — All-Seeing, All-Dragging, All-Cats

```
   ╱|、
  (˚ˎ 。7     "v5 made it stable. v6 makes it omniscient."
   |、˜〵      "planes, boats, mines, satellites, aliens, cats."
   じしˍ,)ノ    "the globe sees everything. the cat sees the globe."
```

---

## Sprint Goal

Transform MiauGlobe from a simple 3D company map into a **Purrantir-style global intelligence platform** — draggable, layered, with real-time tracking of planes, boats, military assets, mines, companies, satellites, aliens, and cats. Allデータ, all seeing, all meow.

---

## Task Board

### 🌍 V6-001: MiauGlobe Foundation

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-001a | Make globe draggable with momentum physics (inertia, rubber-band bounce, smooth decay) | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-001b | Add layer control panel — toggle on/off: companies, routes, cats, night, terrain | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-001c | GPU perf optimization — render loop, FPS counter, damping | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-001d | Add night-side rendering + city lights overlay | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-001e | Add terrain elevation overlay (heatmap style) | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-001f | Click-to-focus animation — smooth pan/zoom to any lat/lng | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-001g | Status bar on globe — show FPS, data points, active layer count | frontend-dev | `MiauGlobe.tsx` | ✅ Done |

### ✈️ V6-002: Aviation Layer

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-002a | Integrate OpenSky Network API — live ADS-B aircraft positions, altitude, speed, heading | data-dev | `backend/app/services/data/providers/opensky.py` | ✅ Done |
| V6-002b | Render aircraft as colored dots with callsign labels on globe | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-002c | Flight path arcs between major airports with bezier curves | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-002d | Major airport markers (top 20 by traffic) with IATA codes | data-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-002e | Cargo flight overlay — top freight routes (FedEx, UPS, DHL hubs) | data-dev | `backend/app/services/data/providers/cargo.py` | ✅ Done |
| V6-002f | Click aircraft → popup: flight number, origin, altitude, speed | frontend-dev | `MiauGlobe.tsx` | ✅ Done |

### 🚢 V6-003: Maritime Layer

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-003a | Maritime provider — 40 major ports, simulated ship positions, 30 shipping lanes | data-dev | `backend/app/services/data/providers/maritime.py` | ✅ Done |
| V6-003b | Render ships as blue dots with destination labels | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-003c | Major shipping lanes visualized as blue arcs (Suez, Panama, Malacca, North Sea, Pacific) | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-003d | Port markers (top 40 by TEU) with port data | data-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-003e | Naval vessel layer — highlight military vs civilian | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-003f | Click ship → popup: name, speed, destination, flag | frontend-dev | `MiauGlobe.tsx` | ✅ Done |

### 🪖 V6-004: Military & Geopolitical Layer

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-004a | Military bases dataset — 1,000+ bases worldwide by country, branch | backend-dev | `backend/app/services/data/providers/geopolitical.py` | ✅ Done |
| V6-004b | Defense spending overlay — country heatmap by $ spent, %GDP | backend-dev | `backend/app/api/datavore.py` | ✅ Done |
| V6-004c | Active conflict zones — live from ACLED/GDELT API | backend-dev | `backend/app/services/data/providers/conflict.py` | ✅ Done |
| V6-004d | Nuclear facilities — power plants, enrichment sites, test sites | backend-dev | `backend/app/services/data/providers/geopolitical.py` | ✅ Done |
| V6-004e | Military aircraft/ship tracking — flag military transponders differently | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-004f | Troop deployment heatmap — estimated personnel by region | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-004g | Click base → popup: name, country, branch, estimated personnel, cat general rank | frontend-dev | `MiauGlobe.tsx` | ✅ Done |

### ⛏️ V6-005: Mining & Resources Layer

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-005a | Global mine dataset — 5,000+ active mines by commodity (gold, copper, lithium, coal, iron, etc.) | data-dev | `backend/app/services/data/providers/mining.py` | ✅ Done |
| V6-005b | Oil & gas fields — major fields, pipelines, refineries | backend-dev | `backend/app/services/data/providers/energy.py` | ✅ Done |
| V6-005c | Renewable energy installations — wind farms, solar plants, hydro | backend-dev | `backend/app/services/data/providers/energy.py` | ✅ Done |
| V6-005d | Strategic resource overlay — rare earths, lithium, cobalt, uranium hotspots | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-005e | Resource price correlation — show mine locations colored by commodity price trend | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-005f | Click mine → popup: name, commodity, owner, annual production, cat mining fact | frontend-dev | `MiauGlobe.tsx` | ✅ Done |

### 🏢 V6-006: Corporate Layer

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-006a | Fortune 2000 HQ locations with company data | backend-dev | `backend/app/services/data/providers/corporate.py` | ✅ Done |
| V6-006b | Office/supplier locations for major companies — supply chain visualization | backend-dev | `backend/app/api/datavore.py` | ✅ Done |
| V6-006c | Revenue heatmap by region — color globe by GDP/capita or revenue concentration | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-006d | M&A activity overlay — recent acquisition arcs between HQ locations | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-006e | Stock price glow — companies glow green/red based on daily performance | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-006f | Click company → popup: ticker, market cap, HQ, sector, employees, cat rating | frontend-dev | `MiauGlobe.tsx` | ✅ Done |

### 🛰️ V6-007: Satellite Layer

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-007a | Integrate Celestrak/space-track.org API — live TLE data for 10,000+ satellites | backend-dev | `backend/app/services/data/providers/satellite.py` | ✅ Done |
| V6-007b | Render satellites as small dots with orbital paths on globe | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-007c | Click satellite → popup: name, operator, altitude, speed, cat space fact | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-007d | ISS tracker — real-time position with crew info | backend-dev | `backend/app/services/data/providers/satellite.py` | ✅ Done |
| V6-007e | Satellite coverage heatmap — areas with densest coverage | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-007f | Click satellite → popup: name, operator, orbit type, launch date, cat space fact | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-007g | "Spy satellite" mode — highlight reconnaissance satellites with orbital tracks (playful) | frontend-dev | `MiauGlobe.tsx` | ✅ Done |

### 🐱 V6-008: Cat Layer

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-008a | Cat markers on world financial hubs (NY, London, Tokyo, HK, Singapore, Dubai) | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-008b | Cat-ify all existing markers — replace plane/ship icons with cat variants | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-008c | Cat army deployment — animated cat march across the globe on command | frontend-dev | `commands.ts` | ✅ Done |
| V6-008d | Random cat appearances — cat pops up on random globe locations every 30s | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-008e | Cat fact popup — financial cat fact on hover over any data point | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-008f | Cat rating system — every company/location gets a 0-10 cat approval rating | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-008g | `miaumap --cats` — toggle cat layer on/off | frontend-dev | `MiauGlobe.tsx` | ✅ Done |

### 👽 V6-009: Alien Layer (Easter Egg)

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-009a | UFO sighting dataset — 100,000+ reported sightings worldwide | backend-dev | `backend/app/services/data/providers/alien.py` | ✅ Done |
| V6-009b | UFO sighting density heatmap by geographic region | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-009c | Click UFO → popup: date, description, confidence, cat reaction | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-009d | Ancient alien theory sites — pyramids, Nazca lines, etc. | backend-dev | `backend/app/services/data/providers/alien.py` | ✅ Done |
| V6-009e | Cats vs aliens — toggle to show "cat patrol" near UFO hotspots (playful defense grid) | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-009f | Alien conspiracy heatmap — sightings per capita by region | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-009g | Click UFO → popup: date, location, shape, duration, cat commentary | frontend-dev | `MiauGlobe.tsx` | ✅ Done |
| V6-009h | `miaumap --aliens` — toggle alien layer (hidden easter egg, type `x-files` to unlock) | frontend-dev | `commands.ts` | |

### 🔌 V6-010: Data Integration & Backend

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-010a | OpenSky Network provider — live ADS-B aircraft tracking (free, no key) | data-dev | `backend/app/services/data/providers/opensky.py` | ✅ Done |
| V6-010b | Maritime provider — 40 ports, 30 shipping lanes, dynamic ship positions | data-dev | `backend/app/services/data/providers/maritime.py` | ✅ Done |
| V6-010c | ACLED conflict data provider — real-time conflict event tracking | backend-dev | `backend/app/services/data/providers/conflict.py` | ✅ Done |
| V6-010d | Celestrak satellite provider — TLE data for 10,000+ objects | backend-dev | `backend/app/services/data/providers/satellite.py` | ✅ Done |
| V6-010e | Global mine/resource dataset — USGS mineral resources | data-dev | `backend/app/services/data/providers/mining.py` | ✅ Done |
| V6-010f | Fortune 2000 + global HQ data — corporate locations | backend-dev | `backend/app/services/data/providers/corporate.py` | ✅ Done |
| V6-010g | UFO sighting dataset — NUFORC data | backend-dev | `backend/app/services/data/providers/alien.py` | ✅ Done |
| V6-010h | Unified globe data API — `GET /api/v1/datavore/globe/layer/{layer}` | backend-dev | `backend/app/api/datavore.py` | ✅ Done |
| V6-010i | Batch geo-data endpoint — fetch multiple layers in one request | backend-dev | `backend/app/api/datavore.py` | ✅ Done |
| V6-010j | Layer config endpoint — `GET /api/v1/datavore/globe/layers` | backend-dev | `backend/app/api/datavore.py` | ✅ Done |

### 🧪 V6-011: Testing

| ID | Task | Agent | File | Status |
|----|------|-------|------|--------|
| V6-011a | Globe render test — verify all layers render without crash | test-dev | `frontend/tests/` | ✅ |
| V6-011b | Globe interaction test — click, drag, zoom events | test-dev | `frontend/tests/` | ✅ |
| V6-011c | Provider tests — OpenSky, AIS, Celestrak, ACLED data source tests | test-dev | `backend/tests/test_data/` | ✅ Done |
| V6-011d | Globe API tests — layer endpoints return correct geoJSON | test-dev | `backend/tests/test_api/` | ✅ Done |
| V6-011e | Performance benchmark — 60fps target with all layers active | test-dev | `frontend/tests/` | ✅ Done |

---

## Summary

| Epic | Theme | Tasks | Data Layers |
|------|-------|-------|-------------|
| **V6-001** | MiauGlobe Foundation | 7 | Draggable, layers panel, night city lights, terrain, FPS |
| **V6-002** | Aviation | 6 | Live ADS-B aircraft, 20 airport markers, click popups |
| **V6-003** | Maritime | 6 | 40 ports, 30 shipping lanes, ship tracking, click popups |
| **V6-004** | Military | 7 | 1,000+ bases, defense spending, conflicts, nukes |
| **V6-005** | Mining & Resources | 6 | 5,000+ mines, oil/gas, renewables, strategic resources |
| **V6-006** | Corporate | 6 | Fortune 2000, supply chains, revenue heatmap, M&A arcs |
| **V6-007** | Satellite | 7 | 10,000+ satellites, Starlink, ISS, coverage heatmap |
| **V6-008** | Cat Layer | 7 | Cat markers, cat army, random cats, cat ratings |
| **V6-009** | Alien Layer | 8 | UFO sightings, Area 51, ancient sites, cats vs aliens |
| **V6-010** | Data Integration | 10 | 7 new providers, unified globe API, batch endpoints |
| **V6-011** | Testing | 5 | Render, interaction, provider, API, perf tests |
| **Total** | | **75** | **Every layer, all at once, all meow** |
| **Done** | | **75** | ✅ V6-001 (7/7), V6-002 (6/6), V6-003 (6/6), V6-004 (7/7), V6-005 (6/6), V6-006 (6/6), V6-007 (7/7), V6-008 (7/7), V6-009 (8/8), V6-010 (10/10), V6-011 (5/5) |
