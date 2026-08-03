import logging
from decimal import Decimal
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.currency_service import get_fx_rate

logger = logging.getLogger(__name__)


async def compute_fx_pnl(
    db: AsyncSession,
    portfolio_id: UUID,
) -> dict:
    portfolio = await db.execute(
        text("SELECT id, base_currency FROM portfolios WHERE id = :pid"),
        {"pid": portfolio_id},
    )
    p = portfolio.mappings().first()
    if not p:
        return {"error": "Portfolio not found"}
    base_currency = p["base_currency"] or "USD"

    positions = await db.execute(
        text("""
            SELECT id, instrument_id, currency, quantity, average_price,
                   cost_basis, market_value, unrealized_pnl, realized_pnl
            FROM positions
            WHERE portfolio_id = :pid AND currency != :base
        """),
        {"pid": portfolio_id, "base": base_currency},
    )
    rows = positions.mappings().all()
    if not rows:
        return {
            "portfolio_id": str(portfolio_id),
            "base_currency": base_currency,
            "fx_positions": 0,
            "total_fx_pnl": 0,
            "total_asset_pnl": 0,
            "details": [],
        }

    total_fx_pnl = Decimal("0")
    results = []
    for pos in rows:
        local_currency = pos["currency"]
        rate = await get_fx_rate(db, local_currency, base_currency)
        if rate is None:
            continue

        entry_value = pos["cost_basis"] or Decimal("0")
        current_value = pos["market_value"] or Decimal("0")
        unrealized = pos["unrealized_pnl"] or Decimal("0")
        realized = pos["realized_pnl"] or Decimal("0")

        total_local_pnl = unrealized + realized

        entry_value_base = entry_value * rate
        current_value_base = current_value * rate
        total_pnl_base = current_value_base - entry_value_base

        fx_pnl = total_pnl_base - total_local_pnl
        total_fx_pnl += fx_pnl

        results.append({
            "instrument_id": str(pos["instrument_id"]),
            "local_currency": local_currency,
            "entry_value_local": float(entry_value),
            "current_value_local": float(current_value),
            "unrealized_pnl_local": float(unrealized),
            "realized_pnl_local": float(realized),
            "total_pnl_local": float(total_local_pnl),
            "fx_rate": float(rate),
            "total_pnl_base": float(total_pnl_base),
            "fx_pnl_component": float(fx_pnl),
            "asset_pnl_component": float(total_local_pnl),
        })

    return {
        "portfolio_id": str(portfolio_id),
        "base_currency": base_currency,
        "fx_positions": len(results),
        "total_fx_pnl": float(total_fx_pnl),
        "total_asset_pnl": sum(r["asset_pnl_component"] for r in results),
        "details": results,
    }


async def record_fx_pnl(
    db: AsyncSession,
    portfolio_id: UUID,
    instrument_id: UUID,
    pnl_amount: Decimal,
    currency: str,
    from_date,
    to_date,
):
    await db.execute(
        text("""
            INSERT INTO pnl (id, portfolio_id, instrument_id, pnl_type, pnl_amount, currency, source, from_date, to_date, attribution)
            VALUES (gen_random_uuid(), :pid, :iid, 'fx', :amount, :currency, 'fx_tracker', :from_date, :to_date,
                    jsonb_build_object('fx_pnl', :amount::text))
            ON CONFLICT DO NOTHING
        """),
        {
            "pid": portfolio_id,
            "iid": instrument_id,
            "amount": pnl_amount,
            "currency": currency,
            "from_date": from_date,
            "to_date": to_date,
        },
    )
    await db.commit()


async def get_pnl_with_fx_breakdown(
    db: AsyncSession,
    portfolio_id: UUID,
    days: int = 30,
) -> dict:
    pnl = await db.execute(
        text("""
            SELECT
                DATE(to_date) as date,
                pnl_type,
                SUM(pnl_amount) as total_pnl,
                COUNT(*) as record_count
            FROM pnl
            WHERE portfolio_id = :pid
              AND to_date >= NOW() - INTERVAL ':days days'
            GROUP BY DATE(to_date), pnl_type
            ORDER BY date DESC
        """),
        {"pid": portfolio_id, "days": days},
    )
    rows = pnl.mappings().all()

    by_type: dict[str, list] = {}
    for r in rows:
        t = r["pnl_type"]
        by_type.setdefault(t, [])
        by_type[t].append({
            "date": str(r["date"]),
            "pnl": float(r["total_pnl"]),
            "count": r["record_count"],
        })

    fx = await compute_fx_pnl(db, portfolio_id)

    return {
        "portfolio_id": str(portfolio_id),
        "pnl_by_type": by_type,
        "fx_breakdown": fx if "error" not in fx else None,
        "current_fx_pnl": fx.get("total_fx_pnl", 0) if "error" not in fx else 0,
    }
