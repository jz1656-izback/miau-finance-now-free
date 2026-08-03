"""Wealth API — net worth, allocation, auto-invest, asset tracking."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.wealth_engine import run_allocation_cycle, get_wealth_summary, get_wealth_transactions
from app.services.treasury_manager import calculate_allocation, check_ops_budget
from app.services.auto_investor import auto_buy_stocks, auto_buy_crypto
from app.services.cloud_credits import buy_cloud_credits, get_cloud_spend_summary
from app.services.real_estate_tracker import get_portfolio_summary, update_penthouse_savings
from app.services.alternative_assets import get_alternative_summary
from app.services.revenue import get_revenue_summary

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/wealth", tags=["Wealth Management"])


@router.get("/summary")
async def wealth_summary(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    revenue = await get_revenue_summary(db)
    wealth = await get_wealth_summary(db)
    real_estate = await get_portfolio_summary(db)
    alts = await get_alternative_summary(db)
    cloud = await get_cloud_spend_summary()
    ops = await check_ops_budget(cloud["estimated_monthly"])
    alloc = await calculate_allocation(revenue.get("total_revenue", 0))
    return {
        "revenue": revenue,
        "wealth": wealth,
        "real_estate": real_estate,
        "alternative_assets": alts,
        "cloud_infrastructure": cloud,
        "ops_budget": ops,
        "allocation_plan": alloc,
    }


@router.post("/allocate")
async def trigger_allocation(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    result = await run_allocation_cycle(db)
    return result


@router.get("/transactions")
async def wealth_transactions(limit: int = Query(20, le=100), db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await get_wealth_transactions(db, limit)


@router.post("/invest/stocks")
async def invest_stocks(
    amount: float = Query(..., description="Amount to invest"),
    dry_run: bool = Query(True),
    user: dict = Depends(get_current_user),
):
    return await auto_buy_stocks(amount, dry_run)


@router.post("/invest/crypto")
async def invest_crypto(
    amount: float = Query(..., description="Amount to invest"),
    dry_run: bool = Query(True),
    user: dict = Depends(get_current_user),
):
    return await auto_buy_crypto(amount, dry_run)


@router.post("/cloud/buy")
async def buy_cloud(
    amount: float = Query(...),
    provider: str = Query("AWS"),
    user: dict = Depends(get_current_user),
):
    return await buy_cloud_credits(amount, provider)


@router.get("/cloud/summary")
async def cloud_summary(user: dict = Depends(get_current_user)):
    return await get_cloud_spend_summary()


@router.get("/realestate")
async def real_estate_summary(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await get_portfolio_summary(db)


@router.get("/alternatives")
async def alternatives_summary(db: AsyncSession = Depends(get_db), user: dict = Depends(get_current_user)):
    return await get_alternative_summary(db)
