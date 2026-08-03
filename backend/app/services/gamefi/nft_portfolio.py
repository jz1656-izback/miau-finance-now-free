import logging
logger = logging.getLogger(__name__)

NFT_HOLDINGS = [
    {"game": "Axie Infinity", "id": "axie_12345", "name": "Mystic Axie", "type": "aquatic", "breed_count": 2, "purchase_price_eth": 0.08, "current_floor_eth": 0.12, "daily_earnings_eth": 0.002},
    {"game": "Axie Infinity", "id": "axie_67890", "name": "Bird Axie", "type": "bird", "breed_count": 1, "purchase_price_eth": 0.05, "current_floor_eth": 0.045, "daily_earnings_eth": 0.001},
    {"game": "The Sandbox", "id": "land_54321", "name": "Sandbox Land #42", "type": "land", "purchase_price_eth": 1.2, "current_floor_eth": 1.5, "daily_earnings_eth": 0.0},
    {"game": "Decentraland", "id": "parcel_999", "name": "DCL Parcel (-12,34)", "type": "parcel", "purchase_price_eth": 2.5, "current_floor_eth": 2.8, "daily_earnings_eth": 0.003},
]

async def get_portfolio() -> dict:
    total_cost = sum(n["purchase_price_eth"] for n in NFT_HOLDINGS)
    total_value = sum(n["current_floor_eth"] for n in NFT_HOLDINGS)
    daily_earnings = sum(n["daily_earnings_eth"] for n in NFT_HOLDINGS)
    return {
        "holdings": NFT_HOLDINGS,
        "total_cost_eth": round(total_cost, 2),
        "total_value_eth": round(total_value, 2),
        "pnl_eth": round(total_value - total_cost, 2),
        "pnl_pct": round((total_value / total_cost - 1) * 100, 1) if total_cost else 0,
        "daily_earnings_eth": round(daily_earnings, 4),
        "monthly_earnings_eth": round(daily_earnings * 30, 4),
        "monthly_earnings_usd": round(daily_earnings * 30 * 3100, 2),
    }

async def get_asset(asset_id: str) -> dict:
    for n in NFT_HOLDINGS:
        if n["id"] == asset_id:
            return n
    return {"error": "Asset not found"}
