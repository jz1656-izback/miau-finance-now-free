"""Carbon footprint API endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.carbon_service import CarbonService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/carbon", tags=["Carbon"])


@router.get("/{ticker}")
async def get_carbon_footprint(
    ticker: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await CarbonService.calculate_intensity(db, ticker)
    if not result:
        raise HTTPException(404, f"No carbon data found for {ticker.upper()}")
    return result


@router.get("/portfolio/{portfolio_id}")
async def get_portfolio_carbon(
    portfolio_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await CarbonService.portfolio_footprint(db, portfolio_id)
    if not result:
        raise HTTPException(404, "Portfolio not found or no carbon data")
    benchmark = await CarbonService.benchmark_comparison(db, portfolio_id)
    return {"footprint": result, "benchmark": benchmark}
