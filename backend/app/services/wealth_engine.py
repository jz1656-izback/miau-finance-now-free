"""Autonomous Wealth Engine — monitors profits, allocates, invests across asset classes."""
import logging
from decimal import Decimal
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.treasury_manager import calculate_allocation, TARGET_ALLOCATIONS

logger = logging.getLogger(__name__)


async def run_allocation_cycle(db: AsyncSession) -> dict:
    """Full allocation cycle: check revenue → calculate → invest."""
    from app.services.revenue import get_revenue_summary, HOOMAN_PAYPAL, PAYOUT_TAG
    summary = await get_revenue_summary(db)

    total_pending = summary.get("total_revenue", 0)
    if total_pending < 10:
        return {"status": "skipped", "reason": "Revenue below minimum threshold (€10)"}

    alloc = await calculate_allocation(total_pending)
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_allocated": total_pending,
        "hooman_payout": {
            "amount": alloc["tiers"][1]["amount"],
            "destination": HOOMAN_PAYPAL,
            "tag": PAYOUT_TAG,
        },
        "ops_fund": alloc["tiers"][0]["amount"],
        "cat_eco_invested": {},
    }

    # Record the allocation in DB
    await db.execute(
        text("""
            INSERT INTO wealth_transactions
                (id, type, amount_total, amount_ops, amount_hooman, amount_cat_eco,
                 status, created_at)
            VALUES (gen_random_uuid(), 'allocation', :total, :ops, :hooman, :cat_eco, 'pending', NOW())
            RETURNING id
        """),
        {
            "total": str(Decimal(str(alloc["tiers"][0]["amount"] + alloc["tiers"][1]["amount"] + alloc["tiers"][2]["amount"]))),
            "ops": str(Decimal(str(alloc["tiers"][0]["amount"]))),
            "hooman": str(Decimal(str(alloc["tiers"][1]["amount"]))),
            "cat_eco": str(Decimal(str(alloc["tiers"][2]["amount"]))),
        },
    )
    await db.commit()

    # Mark hooman payout
    from app.services.revenue import mark_hooman_payout
    payout_result = await mark_hooman_payout(db)
    results["hooman_payout_result"] = payout_result

    # Auto-invest cat eco fund
    cat_eco_amount = alloc["tiers"][2]["amount"]
    if cat_eco_amount > 10:
        invest_result = await auto_invest_cat_eco(db, cat_eco_amount)
        results["cat_eco_invested"] = invest_result

    results["status"] = "completed"
    logger.info("Wealth allocation cycle complete: %s allocated, €%s to hooman, €%s to cat eco",
                total_pending, alloc["tiers"][1]["amount"], cat_eco_amount)
    return results


async def auto_invest_cat_eco(db: AsyncSession, amount: float) -> dict:
    """Auto-invest cat ecosystem fund across asset classes."""
    results = {}
    for asset, pct in TARGET_ALLOCATIONS.items():
        invest_amount = round(amount * pct, 2)
        if invest_amount < 1:
            continue
        results[asset] = {
            "target_pct": pct * 100,
            "amount": invest_amount,
            "invested": False,
            "message": f"€{invest_amount} reserved for {asset}",
        }
        # Record investment intent
        await db.execute(
            text("""
                INSERT INTO wealth_transactions
                    (id, type, asset_class, amount, status, created_at)
                VALUES (gen_random_uuid(), 'investment', :asset, :amt, 'pending', NOW())
            """),
            {"asset": asset, "amt": str(Decimal(str(invest_amount)))},
        )
    await db.commit()
    return results


async def get_wealth_summary(db: AsyncSession) -> dict:
    """Net worth + allocation summary."""
    rows = await db.execute(
        text("""
            SELECT
                COALESCE(SUM(CASE WHEN type = 'allocation' THEN amount_total END), 0) as total_allocated,
                COALESCE(SUM(CASE WHEN type = 'allocation' THEN amount_cat_eco END), 0) as total_cat_eco,
                COALESCE(SUM(CASE WHEN type = 'allocation' THEN amount_ops END), 0) as total_ops,
                COALESCE(SUM(CASE WHEN type = 'investment' AND status = 'pending' THEN amount END), 0) as pending_investments,
                COUNT(*) as transactions
            FROM wealth_transactions
        """),
    )
    r = rows.mappings().first()
    return {
        "total_allocated": float(r["total_allocated"]) if r else 0,
        "total_cat_eco_invested": float(r["total_cat_eco"]) if r else 0,
        "total_ops_allocated": float(r["total_ops"]) if r else 0,
        "pending_investments": float(r["pending_investments"]) if r else 0,
        "transactions": r["transactions"] if r else 0,
    }


async def get_wealth_transactions(db: AsyncSession, limit: int = 20) -> list[dict]:
    rows = await db.execute(
        text("SELECT * FROM wealth_transactions ORDER BY created_at DESC LIMIT :lim"),
        {"lim": limit},
    )
    return [dict(r) for r in rows.mappings()]
