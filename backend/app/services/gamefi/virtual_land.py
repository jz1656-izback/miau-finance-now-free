import logging
logger = logging.getLogger(__name__)

WORLDS = {
    "decentraland": {"name": "Decentraland", "total_parcels": 90601, "avg_price_eth": 2.8, "total_volume_usd": "$520M", "active_landlords": 8500, "premium_areas": ["Crypto Valley", "Fashion District", "Music Plaza"]},
    "sandbox": {"name": "The Sandbox", "total_parcels": 166464, "avg_price_eth": 1.5, "total_volume_usd": "$780M", "active_landlords": 12000, "premium_areas": ["Mecha City", "Dragon Kingdom", "Pixel Plaza"]},
    "somnium": {"name": "Somnium Space", "total_parcels": 5026, "avg_price_eth": 5.2, "total_volume_usd": "$95M", "active_landlords": 1200, "premium_areas": ["Cyber City", "Lake District"]},
    "voxels": {"name": "Voxels (CryptoVoxels)", "total_parcels": 3426, "avg_price_eth": 1.2, "total_volume_usd": "$28M", "active_landlords": 1800, "premium_areas": ["Origin City", "South Block"]},
}

async def list_worlds() -> list[dict]:
    return [{"id": k, **v} for k, v in WORLDS.items()]

async def get_world(world_id: str) -> dict:
    w = WORLDS.get(world_id)
    if not w:
        return {"error": "World not found"}
    return {"id": world_id, **w}

async def portfolio_estimate(parcels: list[dict]) -> dict:
    total_value_eth = 0
    items = []
    for p in parcels:
        world = WORLDS.get(p.get("world", "").lower())
        price = world["avg_price_eth"] if world else 1.0
        multiplier = 1.0
        if p.get("premium"):
            multiplier = 2.5
        if p.get("size", "standard") == "estate":
            multiplier *= 3.0
        value = price * multiplier
        total_value_eth += value
        items.append({"world": p["world"], "parcel": p.get("name", "Unknown"), "value_eth": round(value, 2)})
    return {
        "parcels": items,
        "total_value_eth": round(total_value_eth, 2),
        "total_value_usd": round(total_value_eth * 3100, 2),
        "avg_price_eth": round(total_value_eth / len(parcels), 2) if parcels else 0,
    }

async def price_history(world_id: str) -> list[dict]:
    return [
        {"period": "2025-Q1", "avg_price_eth": 2.2, "sales": 420}, {"period": "2025-Q2", "avg_price_eth": 2.5, "sales": 380},
        {"period": "2025-Q3", "avg_price_eth": 2.8, "sales": 510}, {"period": "2025-Q4", "avg_price_eth": 3.1, "sales": 450},
        {"period": "2026-Q1", "avg_price_eth": 2.8, "sales": 390},
    ] if world_id == "decentraland" else [
        {"period": "2025-Q1", "avg_price_eth": 1.2, "sales": 1200}, {"period": "2025-Q2", "avg_price_eth": 1.4, "sales": 980},
        {"period": "2025-Q3", "avg_price_eth": 1.6, "sales": 1450}, {"period": "2025-Q4", "avg_price_eth": 1.8, "sales": 1100},
        {"period": "2026-Q1", "avg_price_eth": 1.5, "sales": 890},
    ]
