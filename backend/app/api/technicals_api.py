"""Technical Analysis API — indicators, signals, patterns."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.middleware.tier import require_tier
from app.services.analytics.technicals import calculate_technicals, generate_signals_summary

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/technical", tags=["Technical Analysis"])


@router.get("/{ticker}")
async def get_technicals(
    ticker: str,
    period: str = Query("1y", pattern="^(1mo|3mo|6mo|1y|2y)$"),
    user: dict = Depends(get_current_user),
):
    result = await calculate_technicals(ticker.upper(), period)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@router.get("/{ticker}/signal")
async def get_signals(
    ticker: str,
    period: str = Query("1y", pattern="^(1mo|3mo|6mo|1y|2y)$"),
    user: dict = Depends(get_current_user),
    _=Depends(require_tier("pro", "enterprise")),
):
    result = await generate_signals_summary(ticker.upper(), period)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@router.get("/{ticker}/patterns")
async def get_patterns(
    ticker: str,
    period: str = Query("6mo", pattern="^(1mo|3mo|6mo|1y)$"),
    user: dict = Depends(get_current_user),
):
    result = await calculate_technicals(ticker.upper(), period)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return {"ticker": ticker.upper(), "patterns": result.get("patterns", [])}
