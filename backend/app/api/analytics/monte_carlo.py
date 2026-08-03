from fastapi import APIRouter, Query
from app.services.analytics import monte_carlo as mc_service

router = APIRouter()

TICKER_PATTERN = r"^[A-Za-z0-9]{1,10}$"


@router.get("/monte-carlo")
async def monte_carlo(
    ticker: str = Query("AAPL", pattern=TICKER_PATTERN, max_length=10),
    num_simulations: int = Query(1000, ge=100, le=100000),
    days: int = Query(252, ge=10, le=2520),
):
    result = await mc_service.run_monte_carlo(ticker.upper(), num_simulations, days)
    return result
