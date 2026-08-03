from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def create_alert(db: AsyncSession, name: str, metric: str, condition: str,
                       threshold: float, period_minutes: int = 60,
                       channel: str = "dashboard", webhook_url: str | None = None,
                       created_by: str | None = None) -> dict:
    row = await db.execute(text("""
        INSERT INTO marketing_alerts (name, metric, condition, threshold, period_minutes, channel, webhook_url, created_by)
        VALUES (:name, :metric, :condition, :threshold, :period, :channel, :webhook, :created_by)
        RETURNING id, name, metric, condition, threshold, period_minutes, channel, webhook_url, active, last_fired, created_at, created_by
    """), {"name": name, "metric": metric, "condition": condition, "threshold": threshold,
           "period": period_minutes, "channel": channel, "webhook": webhook_url, "created_by": created_by})
    await db.commit()
    return dict(row.mappings().first())


async def list_alerts(db: AsyncSession) -> list[dict]:
    rows = await db.execute(text("""
        SELECT id, name, metric, condition, threshold, period_minutes, channel, webhook_url, active, last_fired, created_at, created_by
        FROM marketing_alerts ORDER BY created_at DESC
    """))
    return [dict(r._mapping) for r in rows]


async def toggle_alert(db: AsyncSession, alert_id: str, active: bool) -> bool:
    row = await db.execute(text("""
        UPDATE marketing_alerts SET active = :active WHERE id = :id RETURNING id
    """), {"active": active, "id": alert_id})
    await db.commit()
    return row.mappings().first() is not None


async def get_alert_history(db: AsyncSession, limit: int = 50) -> list[dict]:
    rows = await db.execute(text("""
        SELECT ah.id, ah.alert_id, ma.name AS alert_name, ah.metric_value, ah.threshold, ah.triggered_at
        FROM alert_history ah
        JOIN marketing_alerts ma ON ma.id = ah.alert_id
        ORDER BY ah.triggered_at DESC LIMIT :lim
    """), {"lim": limit})
    return [dict(r._mapping) for r in rows]
