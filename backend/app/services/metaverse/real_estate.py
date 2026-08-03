import logging
logger = logging.getLogger(__name__)

INDICES = {
    "metaverse": {"name": "Metaverse Land Index", "value": 2450, "change_24h": 1.8, "ytd_pct": 15.2, "description": "Weighted average of all metaverse land prices"},
    "decentraland": {"name": "Decentraland Land Index", "value": 2800, "change_24h": 2.1, "ytd_pct": 18.5, "description": "DCL parcel price index"},
    "sandbox": {"name": "Sandbox Land Index", "value": 1500, "change_24h": -0.5, "ytd_pct": 8.2, "description": "SAND land price index"},
    "somnium": {"name": "Somnium Land Index", "value": 5200, "change_24h": 3.2, "ytd_pct": 22.0, "description": "Somnium parcel price index"},
}

PRIME_LOCATIONS = [
    {"world": "Decentraland", "name": "Crypto Valley", "avg_price_eth": 12.5, "premium_pct": 350, "sales_30d": 18},
    {"world": "Decentraland", "name": "Fashion District", "avg_price_eth": 8.2, "premium_pct": 220, "sales_30d": 25},
    {"world": "The Sandbox", "name": "Mecha City", "avg_price_eth": 5.8, "premium_pct": 280, "sales_30d": 42},
    {"world": "The Sandbox", "name": "Dragon Kingdom", "avg_price_eth": 4.5, "premium_pct": 200, "sales_30d": 35},
    {"world": "Somnium Space", "name": "Cyber City", "avg_price_eth": 18.0, "premium_pct": 250, "sales_30d": 8},
]

async def get_indices() -> dict:
    return INDICES

async def get_index(name: str) -> dict:
    i = INDICES.get(name.lower())
    if not i:
        return {"error": "Index not found"}
    return {"id": name.lower(), **i}

async def prime_locations() -> list[dict]:
    return PRIME_LOCATIONS

async def price_to_earnings() -> dict:
    return {
        "metaverse_avg_pe": 12.5,
        "decentraland_pe": 15.2,
        "sandbox_pe": 10.8,
        "somnium_pe": 18.5,
        "comparison": "Metaverse land P/E ratios are comparable to real-world REITs (avg 15-20x)",
    }
