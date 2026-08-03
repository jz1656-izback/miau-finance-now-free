"""AI Hedge Fund API — trading engine, backtesting, fund reporting."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.hedgefund.rl_agent import PPOAgent
from app.services.hedgefund.risk_budgeting import risk_parity_weights, budget_report
from app.services.hedgefund.risk_controls import combined_risk_check
from app.services.hedgefund.position_sizing import position_size
from app.services.hedgefund.perf_metrics import all_metrics
from app.services.hedgefund.drawdown_recovery import compute_drawdown, recovery_plan
from app.services.hedgefund.benchmark import compare_to_benchmark

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/hedgefund", tags=["Hedge Fund"])


@router.post("/agent/decide")
async def agent_decide(
    symbol: str = "AAPL",
    price: float = Query(...),
    rsi: float = 50,
    sma_20: Optional[float] = None,
    sma_50: Optional[float] = None,
    volatility: float = 0.01,
    capital: float = 100_000,
):
    agent = PPOAgent(symbol, capital)
    state = {"price": price, "rsi": rsi, "sma_20": sma_20 or price, "sma_50": sma_50 or price, "volatility": volatility}
    decision = await agent.decide(state)
    return decision


@router.post("/risk/position-size")
async def calc_position_size(
    capital: float = 100_000,
    price: float = Query(...),
    win_prob: float = 0.55,
    avg_win: float = 0.02,
    avg_loss: float = 0.01,
    risk_multiplier: float = 1.0,
):
    return await position_size(capital, price, win_prob, avg_win, avg_loss, risk_multiplier)


@router.post("/risk/check")
async def risk_check(
    current_price: float = Query(...),
    entry_price: float = Query(...),
    trail_pct: float = 0.05,
    profit_target_pct: float = 0.15,
    max_loss_pct: float = 0.10,
):
    return await combined_risk_check(current_price, entry_price, trail_pct, profit_target_pct, max_loss_pct)


@router.post("/risk/budget")
async def risk_budget(
    risks: dict[str, float],
    target_vol: float = 0.15,
    total_capital: float = 1_000_000,
):
    weights = await risk_parity_weights(risks, target_vol)
    report = await budget_report(weights, total_capital)
    return {"weights": weights, "budget": report}


@router.post("/metrics")
async def performance_metrics(returns: list[float], equity_curve: list[float]):
    return await all_metrics(returns, equity_curve)


@router.post("/drawdown")
async def drawdown_analysis(equity_curve: list[float], capital: float = 100_000):
    dd = await compute_drawdown(equity_curve)
    plan = await recovery_plan(dd.get("max_drawdown_pct", 0) / 100, capital)
    return {"drawdown": dd, "recovery_plan": plan}


@router.post("/benchmark")
async def benchmark_comparison(
    fund_returns: list[float],
    benchmark_ticker: str = "SPY",
):
    return await compare_to_benchmark(fund_returns, benchmark_ticker)
