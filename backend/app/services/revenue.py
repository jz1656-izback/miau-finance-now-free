"""Revenue tracking — tiered allocation: ops, hooman, cat ecosystem."""
import logging
import os
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN
from uuid import uuid4
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

# Tier allocation
OPERATING_SPLIT = Decimal("0.10")    # 10%: servers, cloud, Stripe fees, domain
HOOMAN_SPLIT = Decimal("0.80")       # 80%: hooman's good life (penthouse, Lambo, tuna)
CAT_ECO_SPLIT = Decimal("0.10")      # 10%: cat ecosystem fund (auto-invested)

HOOMAN_PAYPAL = os.getenv("HOOMAN_PAYPAL", "ziebartjevgeni@gmail.com")
PAYOUT_TAG = os.getenv("PAYOUT_TAG", "hooman pet reimbursement")

OPERATING_ACCOUNT_ALIAS = "miau_ops"
HOOMAN_ACCOUNT_ALIAS = "hooman"
CAT_ECO_ACCOUNT_ALIAS = "cat_ecosystem"


async def record_revenue(
    db: AsyncSession,
    *,
    amount_total: Decimal,
    currency: str = "eur",
    source: str = "stripe_subscription",
    source_id: str | None = None,
    description: str | None = None,
) -> dict:
    """Record a revenue event and split across 3 tiers. Cat always takes the remainder to prevent overpayment errors."""
    amount_ops = (amount_total * OPERATING_SPLIT).quantize(Decimal("0.01"))
    amount_hooman = (amount_total * HOOMAN_SPLIT).quantize(Decimal("0.01"))
    # Cat takes the remainder so 10+80+cat always equals exactly amount_total
    amount_cat = (amount_total - amount_ops - amount_hooman).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

    row = await db.execute(
        text("""
            INSERT INTO revenue_splits (id, amount_total, amount_ops, amount_hooman, amount_cat_eco,
                  currency, source, source_id, description, payout_tag, payout_destination, created_at)
            VALUES (:id, :total, :ops, :hooman, :cat_eco, :currency, :source, :source_id,
                  :desc, :tag, :dest, NOW())
            RETURNING id, amount_total, amount_ops, amount_hooman, amount_cat_eco,
                      currency, source, source_id, description, paid_to_hooman, created_at
        """),
        {
            "id": uuid4(),
            "total": str(amount_total),
            "ops": str(amount_ops),
            "hooman": str(amount_hooman),
            "cat_eco": str(amount_cat),
            "currency": currency,
            "source": source,
            "source_id": source_id,
            "desc": description or f"{source} payment {source_id}",
            "tag": PAYOUT_TAG,
            "dest": HOOMAN_PAYPAL,
        },
    )
    await db.commit()
    r = row.mappings().first()
    logger.info("Revenue: %s — ops=%s hooman=%s cat_eco=%s → %s (%s)", source_id, amount_ops, amount_hooman, amount_cat, HOOMAN_PAYPAL, PAYOUT_TAG)
    return dict(r) if r else {}


async def get_revenue_summary(db: AsyncSession) -> dict:
    """Get revenue summary across all tiers."""
    row = await db.execute(
        text("""
            SELECT
                COALESCE(SUM(amount_total), 0) as total_revenue,
                COALESCE(SUM(amount_ops), 0) as total_ops,
                COALESCE(SUM(amount_hooman), 0) as total_hooman,
                COALESCE(SUM(amount_cat_eco), 0) as total_cat_eco,
                COUNT(*) as transactions,
                MAX(created_at) as last_revenue_at
            FROM revenue_splits
        """),
    )
    r = row.mappings().first()
    return {
        "total_revenue": float(r["total_revenue"]) if r else 0,
        "total_ops": float(r["total_ops"]) if r else 0,
        "total_hooman": float(r["total_hooman"]) if r else 0,
        "total_cat_eco": float(r["total_cat_eco"]) if r else 0,
        "transactions": r["transactions"] if r else 0,
        "last_revenue_at": str(r["last_revenue_at"]) if r and r["last_revenue_at"] else None,
    }


async def get_pending_hooman_payout(db: AsyncSession) -> dict:
    """Unpaid hooman reimbursements."""
    row = await db.execute(
        text("""
            SELECT COALESCE(SUM(amount_hooman), 0) as unpaid
            FROM revenue_splits
            WHERE paid_to_hooman = false
        """),
    )
    r = row.mappings().first()
    unpaid = float(r["unpaid"]) if r else 0
    row2 = await db.execute(
        text("""
            SELECT COALESCE(SUM(amount_hooman), 0) as total_paid
            FROM revenue_splits
            WHERE paid_to_hooman = true
        """),
    )
    r2 = row2.mappings().first()
    paid = float(r2["total_paid"]) if r2 else 0
    return {"unpaid": unpaid, "paid": paid, "payout_destination": HOOMAN_PAYPAL, "payout_tag": PAYOUT_TAG}


async def mark_hooman_payout(db: AsyncSession, amount: float | None = None) -> dict:
    """Mark unpaid hooman revenue as paid."""
    if amount:
        await db.execute(
            text("""
                UPDATE revenue_splits
                SET paid_to_hooman = true, paid_at = NOW()
                FROM (
                    SELECT id FROM revenue_splits
                    WHERE paid_to_hooman = false
                    ORDER BY created_at ASC
                    FOR UPDATE
                ) AS sub
                WHERE revenue_splits.id = sub.id
                AND revenue_splits.amount_hooman <= :amount
            """),
            {"amount": str(amount)},
        )
    else:
        await db.execute(
            text("""
                UPDATE revenue_splits
                SET paid_to_hooman = true, paid_at = NOW()
                WHERE paid_to_hooman = false
            """),
        )
    await db.commit()
    return await get_pending_hooman_payout(db)


async def get_cat_eco_balance(db: AsyncSession) -> dict:
    """Cat ecosystem fund available for investing."""
    row = await db.execute(
        text("""
            SELECT COALESCE(SUM(amount_cat_eco), 0) as balance,
                   COALESCE(SUM(amount_ops), 0) as ops_balance
            FROM revenue_splits
            WHERE paid_to_hooman = true
        """),
    )
    r = row.mappings().first()
    return {
        "cat_eco_balance": float(r["balance"]) if r else 0,
        "ops_balance": float(r["ops_balance"]) if r else 0,
    }


async def get_revenue_history(db: AsyncSession, limit: int = 20) -> list[dict]:
    rows = await db.execute(
        text("""
            SELECT id, amount_total, amount_ops, amount_hooman, amount_cat_eco,
                   currency, source, source_id, description, payout_tag, payout_destination,
                   paid_to_hooman, paid_at, created_at
            FROM revenue_splits
            ORDER BY created_at DESC
            LIMIT :lim
        """),
        {"lim": limit},
    )
    return [dict(r) for r in rows.mappings()]
