"""Build complete company database: real tickers + curated + synthetic cover."""
import httpx, json, asyncio, os, random, sys

# ── Exchange → HQ Location mapping ─────────────────────────────
EXCHANGE_MAP: dict[str, tuple[float, float, str, str]] = {
    'NASDAQ': (40.712, -74.006, 'US', 'Tech'),
    'NYSE': (40.754, -73.973, 'US', 'Finance'),
    'AMEX': (40.707, -74.011, 'US', 'Finance'),
    'TSX': (43.653, -79.383, 'CA', 'Finance'),
    'ASX': (-33.868, 151.207, 'AU', 'Finance'),
    'JPX': (35.676, 139.650, 'JP', 'Tech'),
    'BSE': (19.076, 72.877, 'IN', 'Finance'),
    'NSE': (19.076, 72.877, 'IN', 'Tech'),
    'SWX': (47.376, 8.541, 'CH', 'Finance'),
    'TWSE': (25.034, 121.564, 'TW', 'Tech'),
    'HKEX': (22.284, 114.158, 'HK', 'Finance'),
    'LSE': (51.507, -0.127, 'GB', 'Finance'),
    'SIX': (47.376, 8.541, 'CH', 'Finance'),
    'KRX': (37.566, 126.978, 'KR', 'Tech'),
}

EXCHANGE_LIST = list(EXCHANGE_MAP.keys())

# ── Synthetic generators ───────────────────────────────────────
_rng = random.Random(42)
_industries = ["Tech", "Finance", "Healthcare", "Energy", "Consumer", "Industrial",
               "Pharma", "Biotech", "Semiconductors", "Retail", "Food", "RealEstate",
               "Media", "Telecom", "Aerospace", "Logistics", "Mining", "Insurance", "Automotive"]

_prefixes = ["Atlas", "Nova", "Vertex", "Pinnacle", "Meridian", "Crest", "Summit",
    "Apex", "Titan", "Quantum", "Phoenix", "Aurora", "Horizon", "Polaris",
    "Orion", "Vega", "Sapphire", "Cobalt", "Sterling", "Pioneer", "Trident",
    "Legacy", "Catalyst", "Cascade", "Domain", "Elite", "Frontier", "Genesis",
    "Helix", "Integra", "Matrix", "Nexus", "Omega", "Paragon", "Radius",
    "Strata", "Ultima", "Vanguard", "Zenith", "Delta", "Echo", "Fusion",
    "Gravity", "Harmony", "Icon", "Kinetic", "Lumen", "Momentum", "Neural",
    "Optima", "Prism", "Spectrum", "Terra", "Vector", "Wave", "Zen",
    "Bridge", "Circle", "Edge", "Flux", "Grove", "Hub", "Ion", "Jade",
    "Key", "Lynx", "Mesa", "North", "Oak", "Port", "Quest", "Ridge", "Star",
    "Trail", "Unit", "Valley", "West", "Accel", "Bright", "Core", "Deep",
    "Fast", "Green", "High", "Iron", "Lucid", "Prime", "Red", "Safe",
    "Acacia", "Alpine", "Amber", "Anchor", "Arctic", "Arrow", "Aspen", "Avalon",
    "Azure", "Basin", "Bay", "Beacon", "Birch", "Blaze", "Blossom", "Blue",
    "Boulder", "Breeze", "Bronze", "Brook", "Butte", "Canyon", "Capri", "Cardinal",
    "Castle", "Cherry", "Chief", "Citadel", "Citrus", "Cliff", "Clover", "Coast",
    "Comet", "Compass", "Concord", "Copper", "Coral", "Cove", "Crane", "Creek",
    "Crimson", "Cross", "Crown", "Crystal", "Cypress", "Dale", "Dawn", "Denali",
    "Devon", "Diamond", "Dove", "Drake", "Dune", "Eagle", "Eclipse", "Elm",
    "Emerald", "Ember", "Empire", "Equinox", "Everest", "Evergreen", "Falcon",
    "Fern", "Fjord", "Flame", "Flint", "Forge", "Fortress", "Fox", "Frost",
    "Galaxy", "Garnet", "Gate", "Gem", "Glacier", "Glen", "Globe", "Gold",
    "Granite", "Gulf", "Halo", "Harbor", "Haven", "Hawk", "Heath", "Highland",
    "Hill", "Hollow", "Holly", "Ice", "Ivy", "Jasper", "Jazz", "Jewel",
    "Juniper", "Lace", "Lagoon", "Lake", "Lance", "Lantern", "Lark", "Laurel",
    "Liberty", "Lighthouse", "Lilac", "Lily", "Linden", "Lion", "Lodge", "Lotus",
    "Magnet", "Magnolia", "Mallard", "Maple", "Marble", "Marina", "Meadow",
    "Mercury", "Mist", "Monarch", "Moon", "Moss", "Mountain", "Mystic",
    "Nautilus", "Nebula", "Noble", "Nomad", "Oasis", "Ocean", "Olive", "Olympic",
    "Opal", "Onyx", "Orange", "Orbit", "Osprey", "Pacific", "Palm", "Panther",
    "Park", "Pathway", "Patriot", "Peace", "Pearl", "Pebble", "Pelican", "Peak",
    "Pine", "Planet", "Platinum", "Plaza", "Pond", "Prairie", "Quartz", "Rabbit",
    "Raven", "Ravine", "Reef", "Regal", "Ridge", "River", "Riviera", "Robin",
    "Rock", "Rose", "Royal", "Ruby", "Sage", "Sail", "Salt", "Sands", "Satin",
    "Scout", "Sea", "Seal", "Shadow", "Shale", "Shark", "Shell", "Shield",
    "Shore", "Sierra", "Signal", "Silk", "Silver", "Sky", "Slate", "Snow",
    "Solar", "Spirit", "Spruce", "Square", "Starling", "Steel", "Stellar",
    "Storm", "Stream", "Sugar", "Sun", "Sunrise", "Sunset", "Surf", "Swallow",
    "Swan", "Swift", "Talon", "Tempest", "Temple", "Thorne", "Thunder", "Tide",
    "Tiger", "Timber", "Titanium", "Torch", "Tornado", "Tower", "Trail",
    "Tribune", "Trout", "Trust", "Tulip", "Tundra", "Turbo", "Turtle",
    "Union", "Unity", "Valiant", "Valley", "Vapor", "Vault", "Velvet",
    "Venus", "Viceroy", "Victory", "Villa", "Violet", "Viper", "Vista",
    "Volt", "Voyager", "Walnut", "Watch", "Water", "Whale", "Wheel",
    "Wild", "Willow", "Wind", "Wing", "Winter", "Wolf", "Wood", "Wren",
    "Xavier", "Yellow", "Yonder", "Zephyr", "Zion", "Zone",
]
_suffixes = ["Group", "Corp", "Inc", "Systems", "Technologies", "Holdings",
    "International", "Global", "Partners", "Capital", "Ventures", "Industries",
    "Solutions", "Dynamics", "Networks", "Digital", "Innovations", "Enterprises",
    "Analytics", "Services", "Software", "Resources", "Management", "Properties",
    "Brands", "Concepts", "Consulting", "Development", "Equity", "Fund",
    "Futures", "Guild", "Hub", "Institute", "Labs", "Markets", "Media",
    "Platform", "Portfolio", "Research", "Strategies", "Trust", "Works",
    "Advisors", "Alliance", "Commerce", "Exchange", "Finance", "Supplies",
    "Worldwide", "Professionals", "Infrastructure", "Collective"]

def _gen_ticker(existing: set) -> str:
    for _ in range(500):
        length = random.choice([4, 4, 5, 5])
        t = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length))
        if t not in existing:
            existing.add(t)
            return t
    return "ZZZZ"

def _jitter(lat: float, lng: float, r: float = 0.5) -> tuple[float, float]:
    return (lat + random.uniform(-r, r), lng + random.uniform(-r, r))

# ── Cities for uncovered regions ───────────────────────────────
SYNTH_CITIES = {
    "south_america": [(-23.550, -46.633, "BR"), (-22.902, -43.177, "BR"), (-34.603, -58.381, "AR"),
        (-33.448, -70.669, "CL"), (-12.046, -77.042, "PE"), (4.570, -74.297, "CO"),
        (-15.793, -47.879, "BR"), (-34.905, -56.189, "UY"), (-25.286, -57.651, "PY"),
        (-2.170, -79.882, "EC"), (10.480, -66.903, "VE"), (-16.679, -49.255, "BR"),
        (-30.028, -51.228, "BR"), (-7.231, -35.945, "BR"), (-33.045, -71.609, "CL")],
    "africa": [(-33.924, 18.423, "ZA"), (-26.204, 28.041, "ZA"), (30.044, 31.235, "EG"),
        (6.524, 3.379, "NG"), (-1.292, 36.821, "KE"), (-29.858, 31.022, "ZA"),
        (33.573, -7.589, "MA"), (36.806, 10.181, "TN"), (14.693, -17.447, "SN"),
        (5.583, -0.192, "GH"), (9.068, 7.492, "NG"), (-3.383, 36.683, "TZ"),
        (31.042, 31.347, "EG"), (-33.014, 18.502, "ZA"), (6.451, 3.397, "NG")],
    "middle_east": [(24.713, 46.675, "SA"), (25.204, 55.270, "AE"), (24.453, 54.377, "AE"),
        (25.285, 51.531, "QA"), (29.376, 47.971, "KW"), (23.588, 58.382, "OM"),
        (35.694, 51.421, "IR"), (33.312, 44.361, "IQ"), (31.954, 35.936, "JO"),
        (21.543, 39.172, "SA"), (24.366, 54.542, "AE"), (32.081, 34.779, "IL")],
    "europe_extra": [(52.520, 13.405, "DE"), (48.856, 2.352, "FR"), (51.507, -0.127, "GB"),
        (52.370, 4.897, "NL"), (41.893, 12.482, "IT"), (40.416, -3.703, "ES"),
        (47.376, 8.541, "CH"), (55.755, 37.617, "RU"), (59.329, 18.068, "SE"),
        (60.169, 24.938, "FI"), (55.676, 12.568, "DK"), (53.349, -6.260, "IE"),
        (59.913, 10.752, "NO"), (48.208, 16.373, "AT"), (44.426, 26.102, "RO"),
        (52.229, 21.012, "PL"), (50.075, 14.437, "CZ"), (50.850, 4.351, "BE"),
        (38.722, -9.139, "PT"), (45.464, 9.190, "IT"), (55.755, 37.617, "RU")],
    "asia_extra": [(35.676, 139.650, "JP"), (22.543, 113.953, "CN"), (39.904, 116.407, "CN"),
        (1.290, 103.852, "SG"), (13.756, 100.501, "TH"), (14.599, 120.984, "PH"),
        (3.139, 101.686, "MY"), (-6.208, 106.845, "ID"), (21.028, 105.854, "VN"),
        (25.034, 121.564, "TW"), (23.810, 90.412, "BD"), (6.927, 79.861, "LK"),
        (33.684, 73.047, "PK"), (27.717, 85.324, "NP"), (33.590, 130.401, "JP")],
}

async def main():
    existing_tickers = set()
    all_companies = []
    
    # ── Step 1: Fetch real tickers from DumbStockAPI ────────
    print("Fetching real tickers...")
    async with httpx.AsyncClient(timeout=30) as client:
        for ex in EXCHANGE_LIST:
            try:
                r = await client.get(f"https://dumbstockapi.com/stock?exchanges={ex}&format=json")
                if r.status_code != 200: continue
                tickers = r.json()
                lat, lng, country, industry = EXCHANGE_MAP[ex]
                for t in tickers:
                    ticker = (t.get("ticker") or "").strip().upper()
                    name = (t.get("name") or "").strip()
                    if not ticker or not name or ticker in existing_tickers: continue
                    existing_tickers.add(ticker)
                    jlat, jlng = _jitter(lat, lng)
                    all_companies.append((ticker, name[:60], industry, round(jlat,4), round(jlng,4), country, 0))
                print(f"  {ex}: {len(tickers)} → {sum(1 for t in tickers if t.get('ticker','').strip().upper() not in existing_tickers)} new")
            except Exception as e:
                print(f"  {ex}: Error — {e}")
    
    print(f"\nReal tickers: {len(all_companies)}")
    
    # ── Step 2: Add our curated list ─────────────────────────
    # The curated list is in companies_curated.py. We import directly.
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from companies_curated import CURATED  # (ticker, name, industry, lat, lng, country, mc)
        for c in CURATED:
            if c[0] not in existing_tickers:
                existing_tickers.add(c[0])
                all_companies.append(c)
        print(f"Curated added: {len(CURATED)}")
    except Exception as e:
        print(f"Could not load curated: {e}")
    
    # ── Step 3: Generate synthetic for uncovered regions ─────
    target_final = 100_000
    # Distribute remaining slots
    remaining = target_final - len(all_companies)
    region_counts = {
        "south_america": int(remaining * 0.08),
        "africa": int(remaining * 0.06),
        "middle_east": int(remaining * 0.04),
        "europe_extra": int(remaining * 0.12),
        "asia_extra": int(remaining * 0.10),
    }
    assigned = sum(region_counts.values())
    # Add more to US/Canada by jittering from exchange centers
    region_counts["us_extra"] = remaining - assigned  # rest go to US
    us_centers = [(40.712, -74.006, "US"), (34.052, -118.243, "US"), (41.878, -87.636, "US"),
                  (29.760, -95.369, "US"), (37.774, -122.419, "US"), (47.606, -122.332, "US")]
    
    print(f"\nGenerating {remaining} synthetic companies...")
    for region, cities in SYNTH_CITIES.items():
        count = region_counts.get(region, 0)
        for _ in range(count):
            city = random.choice(cities)
            jlat, jlng = _jitter(city[0], city[1], 0.3)
            ticker = _gen_ticker(existing_tickers)
            name = f"{random.choice(_prefixes)} {random.choice(_suffixes)}"
            ind = random.choice(_industries)
            all_companies.append((ticker, name, ind, round(jlat,4), round(jlng,4), city[2], round(random.uniform(0.5, 200), 1)))
    
    # US extra
    for _ in range(region_counts.get("us_extra", 0)):
        city = random.choice(us_centers)
        jlat, jlng = _jitter(city[0], city[1], 1.0)
        ticker = _gen_ticker(existing_tickers)
        name = f"{random.choice(_prefixes)} {random.choice(_suffixes)}"
        ind = random.choice(_industries)
        all_companies.append((ticker, name, ind, round(jlat,4), round(jlng,4), "US", round(random.uniform(0.5, 200), 1)))
    
    # ── Step 4: Write output ─────────────────────────────────
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    frontend_path = os.path.join(root, "frontend", "src", "data", "companies.json")
    flat = [{"t": c[0], "n": c[1], "i": c[2], "lat": c[3], "lng": c[4], "co": c[5], "mc": c[6]} for c in all_companies]
    os.makedirs(os.path.dirname(frontend_path), exist_ok=True)
    with open(frontend_path, "w") as f:
        json.dump({"companies": flat, "total": len(flat)}, f)
    
    size_mb = os.path.getsize(frontend_path) / 1024 / 1024
    print(f"\n🎉 Final: {len(flat)} companies → {frontend_path} ({size_mb:.1f}MB)")
    
    # Also update backend module
    backend_path = os.path.join(root, "backend", "app", "services", "data", "companies_data.py")
    with open(backend_path, "w") as f:
        f.write(f'"""Auto-generated company database — {len(flat)} companies."""\n')
        f.write(f'ALL_COMPANIES: list[tuple] = {json.dumps(all_companies)}\n')
    print(f"Backend data: {backend_path}")

if __name__ == "__main__":
    asyncio.run(main())
