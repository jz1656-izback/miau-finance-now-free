import logging
logger = logging.getLogger(__name__)

OPPORTUNITIES = [
    {"from_world": "Decentraland", "to_world": "The Sandbox", "asset": "Land", "avg_price_gap_pct": 35.0, "profit_potential_pct": 22.0, "confidence": "medium", "volume_30d": 42},
    {"from_world": "The Sandbox", "to_world": "Somnium Space", "asset": "Land", "avg_price_gap_pct": 55.0, "profit_potential_pct": 38.0, "confidence": "low", "volume_30d": 12},
    {"from_world": "Decentraland", "to_world": "Voxels", "asset": "Land", "avg_price_gap_pct": 120.0, "profit_potential_pct": 65.0, "confidence": "medium", "volume_30d": 25},
    {"from_world": "Axie Infinity", "to_world": "Splinterlands", "asset": "NFT", "avg_price_gap_pct": 18.0, "profit_potential_pct": 8.0, "confidence": "high", "volume_30d": 150},
]

async def list_opportunities() -> list[dict]:
    return OPPORTUNITIES

async def detect(world_a: str, world_b: str, asset: str = "Land") -> dict:
    for o in OPPORTUNITIES:
        if world_a.lower() == o["from_world"].lower() and world_b.lower() == o["to_world"].lower():
            return o
    return {"error": "No arbitrage opportunity found between these worlds"}

async def heatmap() -> dict:
    worlds = set()
    for o in OPPORTUNITIES:
        worlds.add(o["from_world"])
        worlds.add(o["to_world"])
    return {"worlds": sorted(worlds), "pair_count": len(OPPORTUNITIES), "best_opportunity": max(OPPORTUNITIES, key=lambda x: x["profit_potential_pct"])}
