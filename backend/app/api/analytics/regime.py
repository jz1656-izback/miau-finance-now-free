from fastapi import APIRouter, Path, Query
from app.services.analytics import regime as regime_service

TICKER_PATTERN = r"^[A-Za-z0-9.]{1,10}$"

router = APIRouter()


@router.get("/regime/{ticker}")
async def detect_regime(
    ticker: str = Path(pattern=TICKER_PATTERN, description="Stock ticker"),
    n_states: int = Query(3, ge=2, le=6, description="Number of hidden regimes"),
    n_iter: int = Query(50, ge=10, le=200, description="EM iterations"),
    period: str = Query("2y", pattern=r"^[0-9]+[dmy]$", description="Historical data period"),
):
    """Detect market regimes for a ticker using Hidden Markov Model.

    Returns the most likely regime sequence (Viterbi decoded),
    state probabilities, transition matrix, and learned parameters
    for each regime (mean return, volatility).

    Default 3 regimes: Bull, Bear, Sideways.
    """
    return await regime_service.detect_regimes(
        ticker=ticker,
        n_states=n_states,
        n_iter=n_iter,
        period=period,
    )
