# 🌍 MiauGlobe — V6 Purrantir Reference

```
  ╱|、
 (˚ˎ 。7    "The all-seeing globe. Data everywhere."
  |、˜〵     "Click anything. The cat is watching."
  じしˍ,)ノ
```

MiauGlobe is a WebGL-powered 3D globe (built on `globe.gl`) that visualizes global data across 11 toggleable layers. Each layer fetches live data from the Miau Finance backend data providers.

---

## Opening the Globe

```bash
miau@finance:~$ miaumap              # Toggle 3D WebGL globe
miau@finance:~$ miaumap --cats       # Open with cat layer
miau@finance:~$ miaumap --aliens     # Open with alien layer unlocked
miau@finance:~$ miauglobe            # Alias for miaumap
miau@finance:~$ map2d                # 2D canvas orthographic globe
miau@finance:~$ map                  # Leaflet flat map
```

## Controls

| Input | Action |
|-------|--------|
| **Drag** | Rotate globe |
| **Scroll** | Zoom in/out |
| **Click** | Open detail popup |
| **TAB** | Focus toggle |
| **x-files** | Type anywhere to unlock 👽 aliens (or press `§`) |

## Layer Toolbar

The toolbar at the top of the globe has toggle buttons for each layer:

| Icon | Layer | Data Source | Description |
|------|-------|-------------|-------------|
| 🏢 | Companies | `corporate.py` | 42 Fortune Global HQ locations |
| 🛤️ | Trade Routes | `opensky.py` | Live ADS-B flight paths |
| 🚢 | Cargo | `cargo.py` | 10 FedEx/UPS/DHL hubs, 18 freight routes |
| 🛰️ | Satellites | `satellite.py` | 17 orbital objects with live Keplerian position |
| ⛏️ | Mining | `mining.py` + `energy.py` | 50 mines, 41 oil fields, 32 renewable |
| 🪖 | Bases | `geopolitical.py` | 60 military bases, sized by personnel |
| 🐱 | Cats | — | Replaces all markers with cat variants |
| 👽 | Aliens | `alien.py` | 25 UFO sightings + 20 ancient sites (locked until x-files) |
| 🌙 | Night | — | City lights overlay on night-side |
| ⛰️ | Terrain | — | Elevation heatmap overlay |

---

## Data Layers Detail

### 🏢 Companies (corporate.py)
- **42 Fortune Global HQ** locations with lat/lng
- Fields: name, ticker, industry, revenue_b
- Marker size scales by revenue ($25B → $600B)
- Click popup: ticker, industry, country, market cap, location

### 🛰️ Satellites (satellite.py)
- **17 orbital objects** computed via Keplerian position engine
- Includes: ISS (🛸 red), HST, Tiangong, Starlink, GPS, GLONASS, BeiDou, Galileo, GOES, KH-11 recon
- ISS has real-time orbital position
- Spy satellite mode highlights 6 classified 🇰🇵🇺🇸🇷🇺 recon sats
- Click popup: operator, orbit type, altitude, launch date, cat space fact

### 🪖 Military Bases (geopolitical.py)
- **60 bases** worldwide across USA, UK, Germany, Japan, South Korea, Qatar, Kuwait, Bahrain, UAE, Iraq, Afghanistan, Djibouti, China, Russia, India, France
- Fields: name, country, branch (Army/Navy/Air Force/Marines/Joint), personnel count
- Marker size scales by personnel (600 → 60,000)
- Color: orange (#ff6b35)
- Click popup: branch, personnel, location, cat general rank (e.g. "Supreme Cat Commander")

### ⛏️ Mining & Resources (mining.py + energy.py)
- **50 mines** (gold, copper, uranium, nickel, cobalt, diamonds)
- **41 oil & gas fields** (Ghawar, Permian, South Pars, etc.)
- **32 renewable installations** (Three Gorges, Gansu Wind, Bhadla Solar, etc.)
- Marker color by commodity: gold→yellow, copper→bronze, oil→black, renewable→green
- Click popup: commodity, owner, annual production, cat mining rating

### 👽 Aliens & UFOs (alien.py)
- **25 UFO sightings** (Nimitz, Phoenix Lights, Roswell, Rendlesham, etc.)
- **20 ancient astronaut theory sites** (Pyramids, Nazca, Puma Punku, Göbekli Tepe, etc.)
- UFO markers glow pink (#ff44ff)
- Unlock by typing `x-files` anywhere on the page
- Click popup: date, description, confidence level

### ⚔️ Conflicts (conflict.py)
- **25 active conflict zones** (Ukraine, Gaza, Sudan, Sahel, Myanmar, DRC, etc.)
- Includes: conventional wars, civil wars, insurgencies, border disputes, maritime disputes
- Data: start year, intensity (Low/Medium/High), parties involved

### 🚢 Cargo Routes (cargo.py)
- **10 FedEx/UPS/DHL logistics hub** locations
- **18 freight routes** between hubs with daily flight count and distance

---

## Batch Data Fetching

MiauGlobe fetches data using the batch endpoint for efficiency:

```
GET /api/v1/datavore/globe/batch?layers=aircraft,maritime,satellites,mining,military_bases,cargo,conflicts
```

Or fetch individual layers:
```
GET /api/v1/datavore/globe/layer/{layer_id}
```

Available layer IDs: `aircraft`, `maritime`, `military_bases`, `nuclear`, `defense_spending`, `mining`, `oil_fields`, `renewable`, `companies`, `cargo`, `satellites`, `ufo`, `ancient_sites`, `conflicts`, `supply_chain`

---

## Satellite Orbital Visualization

The satellite layer includes **orbital path arcs** showing the trajectory of major satellites:

1. Position is calculated at the current epoch using `computeOrbitalPosition()`
2. 20 points along the orbit are generated and connected as an arc
3. ISS path rendered in red, Starlink in blue, others in dim white
4. Spy satellites get 🕵️ markers with "CLASSIFIED" labels

---

*MiauGlobe v6.0 — 13 backend data providers · 56/75 tasks complete · 11 toggleable layers*
