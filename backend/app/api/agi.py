"""AGI Finance API — autonomous trading, risk management, compliance."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.services.agi.executor import (
    execute_decision, approve_execution, reject_execution,
    list_pending, list_history, set_human_in_the_loop, TradeDecision,
)
from app.services.agi.risk_manager import assess_trade_risk, auto_hedge, concentration_report
from app.services.agi.compliance import check_trade

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agi", tags=["AGI"])


@router.post("/trade")
async def agi_trade(
    ticker: str, side: str, qty: float,
    confidence: float = 0.0,
    reasoning: str = "",
    agent_id: str = "",
    user: dict = Depends(get_current_user),
):
    decision = TradeDecision(ticker=ticker.upper(), side=side, qty=qty,
                             confidence=confidence, reasoning=reasoning, agent_id=agent_id)
    return await execute_decision(decision)


@router.post("/approve/{execution_id}")
async def approve(execution_id: str, user: dict = Depends(get_current_user)):
    result = await approve_execution(execution_id)
    if "error" in result:
        raise HTTPException(404, result["error"])
    return result


@router.post("/reject/{execution_id}")
async def reject(execution_id: str, user: dict = Depends(get_current_user)):
    result = await reject_execution(execution_id)
    if "error" in result:
        raise HTTPException(404, result["error"])
    return result


@router.get("/pending")
async def pending(user: dict = Depends(get_current_user)):
    return {"pending": await list_pending()}


@router.get("/history")
async def history(limit: int = 20, user: dict = Depends(get_current_user)):
    return {"executions": await list_history(limit)}


@router.post("/settings")
async def settings(
    human_in_the_loop: bool = True,
    user: dict = Depends(get_current_user),
):
    await set_human_in_the_loop(human_in_the_loop)
    return {"human_in_the_loop": human_in_the_loop}


@router.post("/risk/assess")
async def risk_assess(
    ticker: str, side: str, qty: float, price: float,
    portfolio_value: float = 100000.0,
    user: dict = Depends(get_current_user),
):
    return await assess_trade_risk(ticker.upper(), side, qty, price, portfolio_value)


@router.get("/risk/hedge")
async def hedge(
    portfolio_value: float = 100000.0,
    beta: float = 1.0,
    hedge_pct: float = 0.5,
    user: dict = Depends(get_current_user),
):
    return await auto_hedge(portfolio_value, beta, hedge_pct)


@router.post("/compliance/check")
async def compliance_check(
    ticker: str, side: str, qty: float, price: float,
    portfolio_value: float = 100000.0,
    daily_loss: float = 0.0,
    daily_trades: int = 0,
    user: dict = Depends(get_current_user),
):
    return await check_trade(ticker.upper(), side, qty, price, portfolio_value, daily_loss, daily_trades)


@router.get("/hypotheses")
async def agi_hypotheses(ticker: Optional[str] = Query(None), user: dict = Depends(get_current_user)):
    from app.services.agi.hypothesis_generator import generate_single_hypothesis
    ctx = {"user": user.get("sub", "anonymous")}
    if ticker:
        h = await generate_single_hypothesis(ticker, ctx)
        return {"hypotheses": [h], "count": 1, "ticker": ticker}
    results = []
    for t in ["AAPL", "MSFT", "GOOGL"]:
        h = await generate_single_hypothesis(t, ctx)
        results.append(h)
    return {"hypotheses": results, "count": len(results)}


@router.get("/status")
async def agi_status(user: dict = Depends(get_current_user)):
    return {
        "version": "2.0.0-alpha",
        "human_in_the_loop": True,
        "capabilities": ["autonomous_trading", "risk_management", "compliance", "portfolio_optimization"],
        "status": "operational",
    }
