import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.esg_service import fetch_esg_score, get_portfolio_esg, screen_tickers

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/esg", tags=["ESG"])


@router.get("/{ticker}")
async def esg_ticker_score(
    ticker: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    score = await fetch_esg_score(ticker.upper(), db)
    if score.get("total_score") is None and not score.get("error"):
        raise HTTPException(404, f"No ESG data available for {ticker.upper()}")
    return score


@router.get("/portfolio/{portfolio_id}")
async def esg_portfolio_score(
    portfolio_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return await get_portfolio_esg(portfolio_id, db)


@router.get("/screen")
async def esg_screen(
    min_total: Optional[float] = Query(None, ge=0, le=100),
    max_controversy: Optional[float] = Query(None, ge=0, le=100),
    min_environmental: Optional[float] = Query(None, ge=0, le=100),
    min_social: Optional[float] = Query(None, ge=0, le=100),
    min_governance: Optional[float] = Query(None, ge=0, le=100),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return await screen_tickers(db, min_total, max_controversy, min_environmental, min_social, min_governance, limit)
