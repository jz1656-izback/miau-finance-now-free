import logging
logger = logging.getLogger(__name__)

RENTALS = [
    {"game": "Axie Infinity", "asset_type": "Axie", "avg_daily_rent_eth": 0.003, "avg_apy": 38.0, "available": 12500, "min_days": 7, "utilization_pct": 72},
    {"game": "The Sandbox", "asset_type": "Land", "avg_daily_rent_eth": 0.015, "avg_apy": 22.5, "available": 3200, "min_days": 30, "utilization_pct": 45},
    {"game": "Decentraland", "asset_type": "Parcel", "avg_daily_rent_eth": 0.020, "avg_apy": 18.2, "available": 1800, "min_days": 30, "utilization_pct": 38},
    {"game": "Splinterlands", "asset_type": "Card", "avg_daily_rent_eth": 0.0005, "avg_apy": 55.0, "available": 45000, "min_days": 1, "utilization_pct": 85},
]

async def list_opportunities() -> list[dict]:
    return RENTALS

async def simulate_rental(game: str, asset_value_eth: float, days: int = 30) -> dict:
    for r in RENTALS:
        if game.lower() in r["game"].lower():
            daily_rent = asset_value_eth * (r["avg_apy"] / 100 / 365)
            total_revenue = daily_rent * days
            fee = total_revenue * 0.10
            return {
                "game": r["game"], "asset_value_eth": asset_value_eth, "days": days,
                "daily_rent_eth": round(daily_rent, 6), "total_revenue_eth": round(total_revenue, 4),
                "platform_fee_eth": round(fee, 4), "net_earnings_eth": round(total_revenue - fee, 4),
                "apy": r["avg_apy"],
            }
    return {"error": "Game not found"}
