import logging
logger = logging.getLogger(__name__)

ASSETS = {
    "axie": {"name": "Axie Infinity", "floor_price_eth": 0.012, "avg_price_eth": 0.025, "items": 320000, "daily_volume_eth": 850, "categories": ["aquatic", "beast", "bird", "bug", "dawn", "dusk", "mech", "plant", "reptile"]},
    "sandbox_asset": {"name": "The Sandbox NFT", "floor_price_eth": 0.08, "avg_price_eth": 0.15, "items": 185000, "daily_volume_eth": 320, "categories": ["lands", "avatars", "assets"]},
    "decentraland_wearable": {"name": "Decentraland Wearable", "floor_price_eth": 0.005, "avg_price_eth": 0.015, "items": 520000, "daily_volume_eth": 180, "categories": ["mythic", "legendary", "epic", "rare", "common"]},
}

RARITY_MULTIPLIERS = {"common": 1.0, "rare": 2.5, "epic": 5.0, "legendary": 12.0, "mythic": 30.0}

async def list_assets() -> list[dict]:
    return [{"id": k, **v} for k, v in ASSETS.items()]

async def get_asset(asset_id: str) -> dict:
    a = ASSETS.get(asset_id)
    if not a:
        return {"error": "Asset type not found"}
    return {"id": asset_id, **a}

async def estimate_value(asset_id: str, category: str = "common", quantity: int = 1) -> dict:
    a = ASSETS.get(asset_id)
    if not a:
        return {"error": "Asset type not found"}
    mult = RARITY_MULTIPLIERS.get(category.lower(), 1.0)
    unit_value = a["avg_price_eth"] * mult
    total = unit_value * quantity
    return {
        "asset": a["name"], "category": category, "quantity": quantity,
        "unit_value_eth": round(unit_value, 4), "total_value_eth": round(total, 4),
        "total_value_usd": round(total * 3100, 2), "rarity_bonus_pct": round((mult - 1) * 100, 1),
    }
