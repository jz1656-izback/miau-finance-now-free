from fastapi import APIRouter, Path, Query
from typing import Optional
from app.services.analytics import factors as factors_service

router = APIRouter()


TICKER_PATTERN = r"^[A-Za-z0-9.]{1,10}$"
PERIOD_PATTERN = r"^[0-9]+[dmy]$"


@router.get("/factors/{ticker}")
async def factor_regression(
    ticker: str = Path(pattern=TICKER_PATTERN, description="Stock ticker"),
    model: int = Query(3, ge=3, le=5, description="3-factor or 5-factor model"),
    include_momentum: bool = Query(False, description="Include Momentum (UMD) factor"),
    period: str = Query("2y", pattern=r"^[0-9]+[dmy]$", description="Price history period"),
):
    """Run Fama-French factor regression for a ticker.

    Returns factor loadings (betas), alpha, R², and statistical significance
    for the chosen model (3-factor: Mkt-RF, SMB, HML; 5-factor: + RMW, CMA).
    """
    return await factors_service.run_factor_regression(
        ticker=ticker,
        model=model,
        include_momentum=include_momentum,
        period=period,
    )


@router.get("/factors/{ticker}/summary")
async def factor_summary(
    ticker: str,
    period: str = Query("2y"),
):
    """Quick factor summary — 3-factor with momentum, returns key metrics."""
    return await factors_service.run_factor_regression(
        ticker=ticker, model=3, include_momentum=True, period=period,
    )
