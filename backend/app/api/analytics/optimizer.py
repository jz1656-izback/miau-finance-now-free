from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics import portfolio_optimizer
from app.services.analytics import black_litterman as bl_service
from pydantic import BaseModel

router = APIRouter()


class BlackLittermanView(BaseModel):
    ticker: str
    view_type: str = "absolute"
    q: float = 0.0
    confidence: float = 0.5
    relative_ticker: Optional[str] = None


class BlackLittermanRequest(BaseModel):
    tickers: list[str]
    market_cap_weights: list[float]
    views: list[BlackLittermanView] = []
    risk_aversion: float = 2.5


@router.get("/optimize")
async def optimize(
    tickers: str = Query("AAPL,MSFT,GOOGL", pattern=r"^[A-Z0-9,.]{1,100}$", max_length=100),
    risk_free: float = 0.05,
    period: str = "1y",
):
    t_list = [t.strip() for t in tickers.split(",")]
    return await portfolio_optimizer.optimize_portfolio(t_list, risk_free, period=period)


@router.get("/min-variance")
async def min_variance(tickers: str = Query("AAPL,MSFT,GOOGL", pattern=r"^[A-Z0-9,.]{1,100}$", max_length=100), period: str = "1y"):
    t_list = [t.strip() for t in tickers.split(",")]
    return await portfolio_optimizer.min_variance_portfolio(t_list, period)


@router.get("/equal-weight")
async def equal_weight(tickers: str = Query("AAPL,MSFT,GOOGL", pattern=r"^[A-Z0-9,.]{1,100}$", max_length=100), period: str = "1y"):
    t_list = [t.strip() for t in tickers.split(",")]
    return await portfolio_optimizer.equal_weight_portfolio(t_list, period)


@router.get("/performance")
async def performance(
    tickers: str = Query("AAPL,MSFT,GOOGL", pattern=r"^[A-Z0-9,.]{1,100}$", max_length=100),
    period: str = "1y",
    risk_free: float = 0.05,
):
    from app.services.analytics._yf import get_history
    import pandas as pd
    import numpy as np

    t_list = [t.strip() for t in tickers.split(",")]
    results = {}
    for t in t_list:
        records = await get_history(t, period)
        if not records:
            continue
        closes = [r["close"] for r in records if r.get("close")]
        if len(closes) < 10:
            continue
        r = pd.Series(closes).pct_change().dropna()
        sharpe = portfolio_optimizer.calculate_sharpe(r, risk_free)
        sortino = portfolio_optimizer.calculate_sortino(r, risk_free)
        dd = portfolio_optimizer.calculate_max_drawdown(r)
        results[t] = {
            "sharpe_ratio": sharpe,
            "sortino_ratio": sortino,
            "annualized_return": round(float(r.mean() * 252 * 100), 2),
            "annualized_volatility": round(float(r.std() * np.sqrt(252) * 100), 2),
            **dd,
        }
    return results


@router.post("/black-litterman")
async def black_litterman_endpoint(req: BlackLittermanRequest):
    views_dicts = [v.model_dump() for v in req.views]
    return await bl_service.black_litterman(
        req.tickers, req.market_cap_weights, views_dicts, req.risk_aversion,
    )
