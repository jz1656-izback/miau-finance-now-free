import logging
logger = logging.getLogger(__name__)

EMPLOYMENT = {
    "Decentraland": {"total_jobs": 12500, "growth_qoq_pct": 8.5, "avg_salary_usd": 45000, "top_sectors": ["Events", "Real Estate", "Fashion", "Gaming"]},
    "The Sandbox": {"total_jobs": 18500, "growth_qoq_pct": 12.2, "avg_salary_usd": 52000, "top_sectors": ["Game Dev", "Land Management", "Marketing", "Events"]},
    "Somnium Space": {"total_jobs": 2800, "growth_qoq_pct": 5.5, "avg_salary_usd": 38000, "top_sectors": ["Building", "Events", "Art"]},
    "Spatial": {"total_jobs": 3500, "growth_qoq_pct": 15.0, "avg_salary_usd": 42000, "top_sectors": ["Events", "Education", "Art"]},
}

async def overview() -> dict:
    total = sum(e["total_jobs"] for e in EMPLOYMENT.values())
    return {"total_metaverse_jobs": total, "worlds": EMPLOYMENT}

async def world_employment(world: str) -> dict:
    for name, data in EMPLOYMENT.items():
        if world.lower() in name.lower():
            return {"world": name, **data}
    return {"error": "World not found"}

async def salary_comparison() -> list[dict]:
    return [{"world": w, "avg_salary_usd": d["avg_salary_usd"], "top_role": d["top_sectors"][0]} for w, d in EMPLOYMENT.items()]
