"""Revenue API — 3-tier allocation tracking, payouts, cat eco balance."""
import logging
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.revenue import (
    record_revenue,
    get_revenue_summary,
    get_pending_hooman_payout,
    mark_hooman_payout,
    get_cat_eco_balance,
    get_revenue_history,
    HOOMAN_PAYPAL,
    PAYOUT_TAG,
)
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Revenue"])


class RevenueRecordRequest(BaseModel):
    amount_total: float
    currency: str = "eur"
    source: str = "stripe_subscription"
    source_id: str | None = None
    description: str | None = None


@router.get("/revenue")
async def revenue_summary(db: AsyncSession = Depends(get_db)):
    """Revenue summary across 3 tiers."""
    summary = await get_revenue_summary(db)
    pending = await get_pending_hooman_payout(db)
    cat_eco = await get_cat_eco_balance(db)
    summary["pending_hooman_payout"] = pending["unpaid"]
    summary["total_paid_to_hooman"] = pending["paid"]
    summary["hooman_paypal"] = pending["payout_destination"]
    summary["payout_tag"] = pending["payout_tag"]
    summary["cat_eco_for_investing"] = cat_eco["cat_eco_balance"]
    return summary


@router.get("/revenue/history")
async def revenue_history(db: AsyncSession = Depends(get_db), limit: int = 20):
    return await get_revenue_history(db, limit)


@router.post("/revenue/record")
async def record_revenue_endpoint(
    req: RevenueRecordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    result = await record_revenue(
        db,
        amount_total=Decimal(str(req.amount_total)),
        currency=req.currency,
        source=req.source,
        source_id=req.source_id,
        description=req.description,
    )
    return result


@router.post("/revenue/payout-hooman")
async def payout_hooman(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Mark unpaid hooman revenue as paid."""
    result = await mark_hooman_payout(db)
    return {
        "status": "payout_flagged",
        "payout_destination": HOOMAN_PAYPAL,
        "payout_tag": PAYOUT_TAG,
        "amount": result["unpaid"],
        "total_paid_to_date": result["paid"],
        "message": f"Sent {result['unpaid']}€ to {HOOMAN_PAYPAL} with tag '{PAYOUT_TAG}'",
    }
