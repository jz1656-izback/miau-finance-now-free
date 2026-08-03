from fastapi import APIRouter, Path, Query
from app.services.analytics import pairs as pairs_service

TICKER_PATTERN = r"^[A-Za-z0-9.]{1,10}$"
PERIOD_PATTERN = r"^[0-9]+[dmy]$"

router = APIRouter()


@router.get("/pairs/{ticker_a}/{ticker_b}")
async def analyze_pairs(
    ticker_a: str = Path(pattern=TICKER_PATTERN, description="First ticker"),
    ticker_b: str = Path(pattern=TICKER_PATTERN, description="Second ticker"),
    lookback: int = Query(20, ge=5, le=100, description="Z-score lookback window"),
    period: str = Query("2y", pattern=PERIOD_PATTERN, description="Historical data period"),
):
    """Analyze a pair of tickers for cointegration and trading signals.

    Returns hedge ratio, half-life, ADF test, z-scores, and trading signals
    for the pair (ticker_a, ticker_b).

    A cointegrated pair (ADF p < 0.05) with |z-score| > 2 generates
    trading signals (long/short the spread).
    """
    return await pairs_service.analyze_pair(
        ticker_a=ticker_a,
        ticker_b=ticker_b,
        lookback=lookback,
        period=period,
    )
