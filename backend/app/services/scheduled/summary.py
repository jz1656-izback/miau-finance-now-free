import logging
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.web_push import send_web_push, send_telegram, send_whatsapp

logger = logging.getLogger(__name__)


async def send_daily_summary(db: AsyncSession) -> list[dict]:
    results = []

    subs = await db.execute(
        text("""
            SELECT ps.*, u.username FROM push_subscriptions ps
            JOIN users u ON u.id = ps.user_id
        """),
    )
    subscriptions = subs.mappings().all()

    portfolio_data = await db.execute(
        text("""
            SELECT p.name,
                   COALESCE(SUM(pos.market_value), 0) as total_value,
                   COALESCE(SUM(pos.unrealized_pnl), 0) as total_pnl
            FROM portfolios p
            LEFT JOIN positions pos ON pos.portfolio_id = p.id
            GROUP BY p.id, p.name
            ORDER BY total_value DESC
            LIMIT 3
        """),
    )
    top = portfolio_data.mappings().all()

    market = await db.execute(
        text("SELECT close FROM market_data ORDER BY date DESC LIMIT 1"),
    )
    latest_close = market.scalar() or 0

    lines = ["🐱 Miau Finance — Daily Summary"]
    if top:
        lines.append(f"\nTop Portfolio:")
        for p in top:
            pnl = float(p["total_pnl"] or 0)
            sign = "+" if pnl >= 0 else ""
            lines.append(f"  {p['name']}: ${float(p['total_value'] or 0):,.2f} ({sign}{pnl:,.2f})")
    lines.append(f"\nMarket Close: ${float(latest_close):,.2f}")

    message = "\n".join(lines)

    for sub in subscriptions:
        sub_dict = {
            "endpoint": sub["endpoint"],
            "p256dh_key": sub["p256dh_key"],
            "auth_key": sub["auth_key"],
        }
        ok = await send_web_push(sub_dict, "Daily Market Summary", message)
        results.append({"user": sub["username"], "push_ok": ok})

    return results
