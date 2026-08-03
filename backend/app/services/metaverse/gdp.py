import logging
logger = logging.getLogger(__name__)

WORLDS = ["Decentraland", "The Sandbox", "Somnium Space", "Voxels", "Spatial"]

HISTORICAL = {
    "Decentraland": [{"quarter": "2025-Q1", "gdp_usd": 120_000_000}, {"quarter": "2025-Q2", "gdp_usd": 145_000_000}, {"quarter": "2025-Q3", "gdp_usd": 138_000_000}, {"quarter": "2025-Q4", "gdp_usd": 165_000_000}],
    "The Sandbox": [{"quarter": "2025-Q1", "gdp_usd": 180_000_000}, {"quarter": "2025-Q2", "gdp_usd": 210_000_000}, {"quarter": "2025-Q3", "gdp_usd": 195_000_000}, {"quarter": "2025-Q4", "gdp_usd": 240_000_000}],
    "Somnium Space": [{"quarter": "2025-Q1", "gdp_usd": 22_000_000}, {"quarter": "2025-Q2", "gdp_usd": 28_000_000}, {"quarter": "2025-Q3", "gdp_usd": 25_000_000}, {"quarter": "2025-Q4", "gdp_usd": 32_000_000}],
}

async def overview() -> dict:
    total = sum(sum(h["gdp_usd"] for h in HISTORICAL.get(w, [])) for w in WORLDS)
    latest = {w: HISTORICAL.get(w, [{}])[-1].get("gdp_usd", 0) for w in WORLDS}
    return {"worlds": WORLDS, "total_gdp_all_time_usd": total, "latest_quarter_gdp": latest}

async def world_gdp(world: str) -> list[dict]:
    return HISTORICAL.get(world, [{"error": "World not found"}])

async def total_gdp_by_quarter() -> list[dict]:
    from collections import defaultdict
    quarters = defaultdict(int)
    for world, data in HISTORICAL.items():
        for d in data:
            quarters[d["quarter"]] += d["gdp_usd"]
    return [{"quarter": q, "total_gdp_usd": v} for q, v in sorted(quarters.items())]
