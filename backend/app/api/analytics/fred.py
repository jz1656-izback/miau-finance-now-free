from fastapi import APIRouter, Query
from typing import Optional

from app.config import settings
from app.services.data_sources import fred as fred_service

router = APIRouter()


@router.get("")
async def fred_indicators(
    series_ids: str = Query("GDP,CPIAUCSL,UNRATE,FEDFUNDS,DGS10,DGS2",
                           description="Comma-separated FRED series IDs"),
    limit: int = Query(100, ge=1, le=1000),
):
    api_key = getattr(settings, "fred_api_key", None)
    if not api_key or api_key == "demo":
        from fastapi import HTTPException
        raise HTTPException(400, "FRED API key not configured. Set FRED_API_KEY in .env")
    series_list = [s.strip() for s in series_ids.split(",")]
    return await fred_service.get_observations(series_list, api_key, limit=limit)
