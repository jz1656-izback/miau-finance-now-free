from fastapi import APIRouter, Depends, Query
from typing import Optional
import random
import math
import asyncio
from datetime import timezone, datetime

from app.middleware.auth import get_current_user

router = APIRouter(prefix="/worldmap", tags=["WorldMap"])

CAT_NAMES = ["Whiskers","Mittens","Shadow","Luna","Oliver","Simba","Cleo","Jasper","Nala","Mochi","Felix","Salem","Tiger","Chloe","Milo","Bella","Loki","Oreo","Daisy","Pumpkin","Pepper","Snickers","Tofu","Mochi","Neko","Yuki","Hana","Sora","Kuro","Mimi","Chibi","Tonkatsu","Matcha","Azuki","Wasabi","Nori","Miso","Soba","Mochi2","Panko","Gyoza","Taiyaki","Dorayaki","Onigiri","Edamame","Sashimi","Katsu","Tempura","Ramen","Udon"]
CAT_BREEDS = ["British Shorthair","Siamese","Persian","Maine Coon","Sphynx","Bengal","Ragdoll","Scottish Fold","Abyssinian","Burmese","Russian Blue","Norwegian Forest","Siberian","Turkish Angora","Chartreux"]

MAJOR_CITIES = [
    {"city":"New York","lat":40.71,"lng":-74.01},
    {"city":"London","lat":51.51,"lng":-0.08},
    {"city":"Tokyo","lat":35.69,"lng":139.69},
    {"city":"Shanghai","lat":31.23,"lng":121.47},
    {"city":"Hong Kong","lat":22.32,"lng":114.17},
    {"city":"Singapore","lat":1.35,"lng":103.82},
    {"city":"Sydney","lat":-33.87,"lng":151.21},
    {"city":"Dubai","lat":25.20,"lng":55.27},
    {"city":"Frankfurt","lat":50.11,"lng":8.68},
    {"city":"Paris","lat":48.86,"lng":2.35},
    {"city":"Mumbai","lat":19.08,"lng":72.88},
    {"city":"São Paulo","lat":-23.55,"lng":-46.63},
    {"city":"Toronto","lat":43.65,"lng":-79.38},
    {"city":"Seoul","lat":37.57,"lng":126.98},
    {"city":"Moscow","lat":55.76,"lng":37.62},
    {"city":"Zurich","lat":47.38,"lng":8.54},
    {"city":"Johannesburg","lat":-26.20,"lng":28.05},
    {"city":"Mexico City","lat":19.43,"lng":-99.13},
    {"city":"Jakarta","lat":-6.21,"lng":106.85},
    {"city":"Istanbul","lat":41.01,"lng":28.98},
]


def _generate_cats() -> list[dict]:
    random.seed(42)
    cats = []
    names = random.sample(CAT_NAMES, min(50, len(CAT_NAMES)))
    for i, name in enumerate(names):
        city = MAJOR_CITIES[i % len(MAJOR_CITIES)]
        lat = city["lat"] + random.uniform(-1, 1)
        lng = city["lng"] + random.uniform(-1, 1)
        cats.append({
            "name": name,
            "breed": random.choice(CAT_BREEDS),
            "lat": round(lat, 3),
            "lng": round(lng, 3),
            "net_worth": random.randint(10000, 5000000),
            "city": city["city"],
            "is_captain": i < 10,
        })
    return cats


@router.get("/live")
async def worldmap_live(
    user: dict | None = None,
):
    data: dict = {"countries": [], "trade_routes": [], "capital_flows": [], "space": {}, "cats": _generate_cats(), "cat_commentary": ""}

    # Countries — try World Bank GDP
    gdp_map: dict[str, float] = {}
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get("http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json&per_page=300&mrnev=1")
            if resp.status_code == 200:
                wb = resp.json()
                for entry in wb[1] if len(wb) > 1 else []:
                    iso = entry.get("countryiso3code", "")
                    val = entry.get("value")
                    if iso and val:
                        gdp_map[iso] = round(val / 1e9, 1)
    except Exception:
        pass

    country_map: dict = {
        "US":{"name":"USA","index_change":0.38,"is_open":True},
        "GB":{"name":"UK","index_change":-0.21,"is_open":True},
        "JP":{"name":"Japan","index_change":-0.45,"is_open":False},
        "DE":{"name":"Germany","index_change":0.15,"is_open":True},
        "FR":{"name":"France","index_change":0.33,"is_open":True},
        "CN":{"name":"China","index_change":0.65,"is_open":False},
        "IN":{"name":"India","index_change":1.20,"is_open":True},
        "BR":{"name":"Brazil","index_change":-0.72,"is_open":True},
        "CH":{"name":"Switzerland","index_change":0.08,"is_open":True},
        "AU":{"name":"Australia","index_change":0.52,"is_open":False},
    }
    for iso, c in country_map.items():
        c["iso"] = iso
        c["gdp"] = gdp_map.get(iso, 0)
        data["countries"].append(c)

    # Trade routes
    routes = [
        ("US","GB",4200,1.2,"🐱🚢"), ("US","JP",3800,0.9,"😼⛴️"), ("US","CN",3500,1.1,"🐱🚢"),
        ("GB","DE",1800,0.7,"😺🛳️"), ("GB","CH",1200,0.5,"🐈⛵"),
        ("CN","JP",2900,1.3,"🐱🚢"), ("CN","IN",1600,1.0,"😼⛴️"),
        ("JP","AU",1100,0.6,"😺🛳️"), ("US","BR",800,0.4,"😿🚤"),
        ("DE","CN",900,0.8,"🐈⛵"), ("US","IN",700,1.1,"🐱🚢"),
        ("GB","FR",600,0.5,"😺🛳️"),
    ]
    for frm, to, vol, vel, boat in routes:
        data["trade_routes"].append({"from": frm, "to": to, "volume": vol, "velocity": vel, "catboat": boat})

    # Capital flows
    flows = [("GB","US",850,"🐱✈️"),("JP","US",620,"🐱✈️"),("CH","US",480,"🐱✈️"),("DE","US",350,"🐱✈️"),("CN","US",290,"🐱✈️")]
    for frm, to, amt, jet in flows:
        data["capital_flows"].append({"from": frm, "to": to, "amount": amt, "jet": jet})

    # Space
    try:
        import httpx
        async with httpx.AsyncClient(timeout=3) as client:
            iss_resp = await client.get("http://api.open-notify.org/iss-now.json")
            if iss_resp.status_code == 200:
                iss = iss_resp.json().get("iss_position", {})
                data["space"]["iss"] = {"lat": float(iss.get("latitude", 0)), "lng": float(iss.get("longitude", 0)), "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception:
        data["space"]["iss"] = {"lat": -33.8, "lng": 151.2, "timestamp": datetime.now(timezone.utc).isoformat()}

    data["space"]["launches"] = [
        {"mission":"Starlink 6-42","rocket":"Falcon 9","date":"2026-05-22","pad":"SLC-40","lat":28.56,"lng":-80.58},
        {"mission":"CRS-31","rocket":"Falcon 9","date":"2026-05-25","pad":"LC-39A","lat":28.61,"lng":-80.60},
        {"mission":"Starship Test","rocket":"Starship","date":"2026-06-01","pad":"Starbase","lat":25.99,"lng":-97.18},
    ]
    data["space"]["launch_pads"] = [
        {"name":"Kennedy LC-39A","lat":28.61,"lng":-80.60},
        {"name":"Cape Canaveral SLC-40","lat":28.56,"lng":-80.58},
        {"name":"Vandenberg SLC-4E","lat":34.63,"lng":-120.61},
        {"name":"Starbase Boca Chica","lat":25.99,"lng":-97.18},
    ]

    # Cat commentary
    data["cat_commentary"] = random.choice([
        "🐱 The cat is monitoring global markets. Treat jar at 47%.",
        "🐱 ISS just passed over Tokyo. The cat waved.",
        "🐱 Catboat traffic is heavy in the Atlantic. The cat recommends patience.",
        "🐱 The cat sees a smart money jet heading to New York. Something big is happening.",
        "🐱 Whiskers the cat has been spotted near SpaceX. Is the cat going to space?",
    ])

    # Commodities — realistic prices with random walk
    seed = int(datetime.now(timezone.utc).timestamp() / 60)
    rng = random.Random(seed)
    data["commodities"] = [
        {"name": "Crude Oil (WTI)", "symbol": "CL", "price": round(78.50 + rng.uniform(-1.5, 1.5), 2), "unit": "USD/bbl", "change_pct": round(rng.uniform(-2.5, 2.5), 2), "lat": 31.9, "lng": -102.9, "icon": "🛢️"},
        {"name": "Brent Crude", "symbol": "BNO", "price": round(82.30 + rng.uniform(-1.2, 1.2), 2), "unit": "USD/bbl", "change_pct": round(rng.uniform(-2.0, 2.0), 2), "lat": 58.0, "lng": 2.0, "icon": "🛢️"},
        {"name": "Gold", "symbol": "XAU", "price": round(2320 + rng.uniform(-20, 20), 2), "unit": "USD/oz", "change_pct": round(rng.uniform(-1.5, 1.5), 2), "lat": -26.2, "lng": 28.0, "icon": "🥇"},
        {"name": "Silver", "symbol": "XAG", "price": round(28.50 + rng.uniform(-0.8, 0.8), 2), "unit": "USD/oz", "change_pct": round(rng.uniform(-3.0, 3.0), 2), "lat": 23.0, "lng": -102.0, "icon": "🥈"},
        {"name": "Copper", "symbol": "HG", "price": round(4.85 + rng.uniform(-0.15, 0.15), 2), "unit": "USD/lb", "change_pct": round(rng.uniform(-2.0, 2.0), 2), "lat": -22.0, "lng": -68.0, "icon": "🪙"},
        {"name": "Iron Ore", "symbol": "SI", "price": round(108.50 + rng.uniform(-3, 3), 2), "unit": "USD/t", "change_pct": round(rng.uniform(-2.5, 2.5), 2), "lat": -26.0, "lng": 134.0, "icon": "⛏️"},
        {"name": "Natural Gas", "symbol": "NG", "price": round(2.75 + rng.uniform(-0.15, 0.15), 2), "unit": "USD/MMBtu", "change_pct": round(rng.uniform(-4.0, 4.0), 2), "lat": 42.0, "lng": -80.0, "icon": "🔥"},
        {"name": "Wheat", "symbol": "ZW", "price": round(6.20 + rng.uniform(-0.30, 0.30), 2), "unit": "USD/bu", "change_pct": round(rng.uniform(-3.0, 3.0), 2), "lat": 46.0, "lng": -100.0, "icon": "🌾"},
        {"name": "Corn", "symbol": "ZC", "price": round(4.60 + rng.uniform(-0.20, 0.20), 2), "unit": "USD/bu", "change_pct": round(rng.uniform(-3.0, 3.0), 2), "lat": 41.0, "lng": -93.0, "icon": "🌽"},
        {"name": "Coffee", "symbol": "KC", "price": round(2.35 + rng.uniform(-0.10, 0.10), 2), "unit": "USD/lb", "change_pct": round(rng.uniform(-2.0, 2.0), 2), "lat": -15.0, "lng": -47.0, "icon": "☕"},
        {"name": "Lithium", "symbol": "LIT", "price": round(13.20 + rng.uniform(-0.50, 0.50), 2), "unit": "USD/kg", "change_pct": round(rng.uniform(-5.0, 5.0), 2), "lat": -23.0, "lng": -67.0, "icon": "🔋"},
        {"name": "Uranium", "symbol": "U3O8", "price": round(72.00 + rng.uniform(-2, 2), 2), "unit": "USD/lb", "change_pct": round(rng.uniform(-3.0, 3.0), 2), "lat": 56.0, "lng": -106.0, "icon": "☢️"},
    ]

    # Bond yields — realistic 10Y government bond yields with daily walk
    data["bond_yields"] = [
        {"country": "US", "yield": round(4.38 + rng.uniform(-0.05, 0.05), 2), "name": "US Treasury 10Y", "lat": 38.9, "lng": -77.0, "change_bps": round(rng.uniform(-8, 8))},
        {"country": "GB", "yield": round(4.12 + rng.uniform(-0.04, 0.04), 2), "name": "UK Gilt 10Y", "lat": 51.5, "lng": -0.1, "change_bps": round(rng.uniform(-6, 6))},
        {"country": "DE", "yield": round(2.48 + rng.uniform(-0.03, 0.03), 2), "name": "German Bund 10Y", "lat": 52.5, "lng": 13.4, "change_bps": round(rng.uniform(-5, 5))},
        {"country": "FR", "yield": round(2.87 + rng.uniform(-0.03, 0.03), 2), "name": "France OAT 10Y", "lat": 48.9, "lng": 2.3, "change_bps": round(rng.uniform(-5, 5))},
        {"country": "JP", "yield": round(0.97 + rng.uniform(-0.02, 0.02), 2), "name": "Japan JGB 10Y", "lat": 35.7, "lng": 139.7, "change_bps": round(rng.uniform(-3, 3))},
        {"country": "CH", "yield": round(0.68 + rng.uniform(-0.02, 0.02), 2), "name": "Swiss 10Y", "lat": 47.0, "lng": 8.0, "change_bps": round(rng.uniform(-4, 4))},
        {"country": "AU", "yield": round(4.22 + rng.uniform(-0.04, 0.04), 2), "name": "Australia 10Y", "lat": -35.3, "lng": 149.1, "change_bps": round(rng.uniform(-6, 6))},
        {"country": "CA", "yield": round(3.51 + rng.uniform(-0.04, 0.04), 2), "name": "Canada 10Y", "lat": 45.4, "lng": -75.7, "change_bps": round(rng.uniform(-6, 6))},
        {"country": "IN", "yield": round(7.05 + rng.uniform(-0.06, 0.06), 2), "name": "India 10Y", "lat": 28.6, "lng": 77.2, "change_bps": round(rng.uniform(-10, 10))},
        {"country": "BR", "yield": round(11.87 + rng.uniform(-0.08, 0.08), 2), "name": "Brazil 10Y", "lat": -15.8, "lng": -47.9, "change_bps": round(rng.uniform(-12, 12))},
        {"country": "CN", "yield": round(2.56 + rng.uniform(-0.03, 0.03), 2), "name": "China 10Y", "lat": 39.9, "lng": 116.4, "change_bps": round(rng.uniform(-5, 5))},
    ]

    return data
