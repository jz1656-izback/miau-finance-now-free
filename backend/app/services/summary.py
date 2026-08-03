"""Daily portfolio summary service.

Generates a concise daily snapshot: portfolio value, P&L, top movers,
market context, and recent activity. Designed for the ``summary``
terminal command and ``GET /api/v1/summary``.
"""

import logging
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def get_daily_summary(
    db: AsyncSession,
    user_id: str,
    summary_date: Optional[date] = None,
) -> dict[str, Any]:
    when = summary_date or date.today()
    today_start = datetime.combine(when, datetime.min.time(), tzinfo=timezone.utc)
    month_start = today_start.replace(day=1)

    # Portfolio overview
    portfolios = await db.execute(
        text("""
            SELECT p.id, p.name, p.base_currency,
                   COALESCE(SUM(pos.market_value), 0) AS total_value,
                   COALESCE(SUM(pos.unrealized_pnl), 0) AS total_unrealized,
                   COALESCE(SUM(pos.realized_pnl), 0) AS total_realized
            FROM portfolios p
            JOIN positions pos ON pos.portfolio_id = p.id
            WHERE p.id IN (
                SELECT id FROM portfolios
            )
            GROUP BY p.id, p.name, p.base_currency
            ORDER BY total_value DESC
        """),
    )
    pf_list = [dict(r) for r in portfolios.mappings().all()]

    # Top movers (positions with largest |change| today)
    top_movers = await db.execute(
        text("""
            SELECT pos.ticker,
                   pos.market_value - pos.cost_basis AS pnl,
                   CASE WHEN pos.cost_basis > 0
                        THEN (pos.market_value - pos.cost_basis) / pos.cost_basis * 100
                        ELSE 0 END AS pct_change
            FROM positions pos
            WHERE pos.portfolio_id IN (
                SELECT id FROM portfolios
            )
            ORDER BY ABS(pnl) DESC
            LIMIT 5
        """),
    )
    movers = [dict(r) for r in top_movers.mappings().all()]

    # Today's orders
    orders_today = await db.execute(
        text("""
            SELECT COUNT(*) AS count,
                   COALESCE(SUM(CASE WHEN side = 'BUY' THEN 1 ELSE 0 END), 0) AS buys,
                   COALESCE(SUM(CASE WHEN side = 'SELL' THEN 1 ELSE 0 END), 0) AS sells
            FROM orders
            WHERE created_at >= :today
        """),
        {"today": today_start},
    )
    orders = orders_today.mappings().first()

    # Month-to-date P&L
    mtd_pnl = await db.execute(
        text("""
            SELECT COALESCE(SUM(pnl_amount), 0) AS mtd
            FROM pnl
            WHERE created_at >= :month_start AND pnl_type = 'REALIZED'
        """),
        {"month_start": month_start},
    )
    mtd = mtd_pnl.mappings().first()

    # Recent activity
    recent = await db.execute(
        text("""
            SELECT action, resource_type, created_at
            FROM activity_logs
            WHERE user_id = :uid AND created_at >= :today
            ORDER BY created_at DESC
            LIMIT 10
        """),
        {"uid": user_id, "today": today_start},
    )

    total_value = sum(float(p["total_value"] or 0) for p in pf_list)
    total_pnl = sum(float(p["total_unrealized"] or 0) + float(p["total_realized"] or 0) for p in pf_list)

    return {
        "date": when.isoformat(),
        "portfolios": [
            {
                "id": str(p["id"]),
                "name": p["name"],
                "currency": p["base_currency"],
                "value": float(p["total_value"] or 0),
                "unrealized_pnl": float(p["total_unrealized"] or 0),
                "realized_pnl": float(p["total_realized"] or 0),
            }
            for p in pf_list
        ],
        "totals": {
            "portfolio_count": len(pf_list),
            "total_value": round(total_value, 2),
            "total_pnl": round(total_pnl, 2),
            "pnl_pct": round((total_pnl / total_value * 100) if total_value else 0, 2),
            "mtd_realized_pnl": round(float(mtd["mtd"] or 0), 2),
        },
        "top_movers": [
            {
                "ticker": m["ticker"],
                "pnl": round(float(m["pnl"] or 0), 2),
                "pct_change": round(float(m["pct_change"] or 0), 2),
            }
            for m in movers
        ],
        "orders_today": {
            "total": orders["count"] if orders else 0,
            "buys": orders["buys"] if orders else 0,
            "sells": orders["sells"] if orders else 0,
        },
        "recent_activity": [
            {
                "action": r["action"],
                "resource": r["resource_type"],
                "time": r["created_at"].isoformat() if r["created_at"] else None,
            }
            for r in recent.mappings().all()
        ],
    }
