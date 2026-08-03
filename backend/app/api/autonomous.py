"""Autonomous Wealth Engine API — status, trigger, log."""
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.wealth_engine import run_allocation_cycle
from app.services.auto_investor import auto_buy_stocks, auto_buy_crypto

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/autonomous", tags=["Autonomous"])


@router.get("/status")
async def autonomous_status(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    from app.services.wealth_engine import get_wealth_summary
    wealth = await get_wealth_summary(db)
    return {
        "engine": "Miau Autonomous Wealth Engine",
        "version": "1.0.0",
        "status": "active",
        "total_allocated": wealth.get("total_allocated", 0),
        "cat_eco_invested": wealth.get("total_cat_eco_invested", 0),
        "last_allocation": "See /wealth/transactions for history",
        "scheduler": "Weekly (every Sunday at 00:00)",
        "human_in_loop": True,
        "investors": ["Stocks (Alpaca)", "Crypto (ETH/BTC)", "Cloud Credits (AWS)"],
        "cat_commentary": "The autonomous wealth engine is watching. The cat is supervising. 🐱",
    }


@router.post("/trigger")
async def trigger_autonomous(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    result = await run_allocation_cycle(db)
    return result


@router.post("/invest/stocks")
async def autonomous_invest_stocks(
    amount: float = 1000,
    dry_run: bool = True,
    user: dict = Depends(get_current_user),
):
    return await auto_buy_stocks(amount, dry_run)


@router.post("/invest/crypto")
async def autonomous_invest_crypto(
    amount: float = 1000,
    dry_run: bool = True,
    user: dict = Depends(get_current_user),
):
    return await auto_buy_crypto(amount, dry_run)
