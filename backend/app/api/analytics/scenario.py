from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.middleware.auth import get_current_user
from app.services.analytics.scenario import run_scenario, portfolio_scenario

router = APIRouter(prefix="/scenario", tags=["Scenario Analysis"])


@router.get("/{ticker}")
async def api_scenario(
    ticker: str,
    user: dict = Depends(get_current_user),
):
    return await run_scenario(ticker)


@router.post("/portfolio")
async def api_portfolio_scenario(
    tickers: list[str] = Query(...),
    weights: Optional[str] = Query(None, description="Comma-separated weights matching tickers"),
    market_shock: float = Query(-0.10, ge=-0.50, le=0.50, description="Market shock (-0.10 = 10% drop)"),
    user: dict = Depends(get_current_user),
):
    weight_list = None
    if weights:
        weight_list = [float(w.strip()) for w in weights.split(",") if w.strip()]
    return await portfolio_scenario(tickers, weight_list, market_shock)


@router.get("/shocks/{ticker}")
async def api_shocks(
    ticker: str,
    shocks: str = Query("-0.20,-0.10,0,0.10,0.20,-0.40", description="Comma-separated shock values"),
    user: dict = Depends(get_current_user),
):
    shock_list = [float(s.strip()) for s in shocks.split(",") if s.strip()]
    shock_scenarios = [{"label": f"Shock {s:+.0%}", "shock": s, "beta_mult": 1.0} for s in shock_list]
    return await run_scenario(ticker, shocks=shock_scenarios)
