"""Real Estate Tracker — property holdings, valuations, penthouse fund."""
import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

PENTHOUSE_TARGET = 1_500_000  # €1.5M penthouse goal
LAMBO_COST = 350_000  # €350K Lamborghini


async def track_property(db: AsyncSession, name: str, value: float, mortgage: float = 0, rental_income: float = 0) -> dict:
    """Add or update a real estate asset."""
    await db.execute(
        text("""
            INSERT INTO real_estate_assets (id, name, current_value, mortgage_balance, monthly_rental_income, last_valuation, created_at)
            VALUES (gen_random_uuid(), :name, :value, :mortgage, :rental, NOW(), NOW())
            ON CONFLICT (name) DO UPDATE SET
                current_value = :value2, mortgage_balance = :mortgage2,
                monthly_rental_income = :rental2, last_valuation = NOW()
            RETURNING id
        """),
        {"name": name, "value": value, "mortgage": mortgage, "rental": rental_income,
         "value2": value, "mortgage2": mortgage, "rental2": rental_income},
    )
    await db.commit()
    return {"name": name, "value": value, "status": "tracked"}


async def get_portfolio_summary(db: AsyncSession) -> dict:
    """Get real estate portfolio summary + penthouse progress."""
    rows = await db.execute(
        text("""
            SELECT COALESCE(SUM(current_value), 0) as total_value,
                   COALESCE(SUM(mortgage_balance), 0) as total_mortgage,
                   COALESCE(SUM(monthly_rental_income), 0) as total_rental_income,
                   COUNT(*) as properties
            FROM real_estate_assets
        """),
    )
    r = rows.mappings().first()
    total_value = float(r["total_value"]) if r else 0
    total_mortgage = float(r["total_mortgage"]) if r else 0
    equity = total_value - total_mortgage
    return {
        "total_value": total_value,
        "total_mortgage": total_mortgage,
        "equity": equity,
        "monthly_rental_income": float(r["total_rental_income"]) if r else 0,
        "properties": r["properties"] if r else 0,
        "penthouse_progress": {
            "target": PENTHOUSE_TARGET,
            "current_savings": 0,  # Mainly from hooman's share
            "remaining": PENTHOUSE_TARGET,
            "pct_complete": 0,
            "lambo_fund": {
                "target": LAMBO_COST,
                "current": 0,
                "remaining": LAMBO_COST,
            },
        },
    }


async def update_penthouse_savings(db: AsyncSession, hooman_payout_amount: float) -> dict:
    """Track penthouse + lambo savings from hooman payouts."""
    pct_to_penthouse = 0.6   # 60% of hooman payout → penthouse
    pct_to_lambo = 0.15      # 15% → Lamborghini
    pct_to_life = 0.25       # 25% → good life (tuna, bills, fun)

    to_penthouse = round(hooman_payout_amount * pct_to_penthouse, 2)
    to_lambo = round(hooman_payout_amount * pct_to_lambo, 2)
    to_life = round(hooman_payout_amount * pct_to_life, 2)

    return {
        "payout_amount": hooman_payout_amount,
        "penthouse_fund": to_penthouse,
        "lambo_fund": to_lambo,
        "good_life_fund": to_life,
        "penthouse_target": PENTHOUSE_TARGET,
        "lambo_target": LAMBO_COST,
        "message": f"€{to_penthouse} → penthouse, €{to_lambo} → Lambo, €{to_life} → good life",
    }
