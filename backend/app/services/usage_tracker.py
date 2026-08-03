import logging
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def log_api_usage(
    db: AsyncSession,
    user_id: str,
    endpoint: str,
    method: str,
    status_code: int,
    latency_ms: float,
    api_key_id: str = None,
):
    await db.execute(
        text("""
            INSERT INTO api_usage_log (id, user_id, api_key_id, endpoint, method, status_code, latency_ms)
            VALUES (gen_random_uuid(), :uid, :key_id, :endpoint, :method, :status, :latency)
        """),
        {
            "uid": user_id,
            "key_id": api_key_id,
            "endpoint": endpoint,
            "method": method,
            "status": status_code,
            "latency": latency_ms,
        },
    )
    await db.commit()


async def get_usage_stats(
    db: AsyncSession,
    user_id: str = None,
    period: str = "daily",
) -> dict:
    interval = {"daily": "1 day", "weekly": "7 days", "monthly": "30 days"}.get(period, "1 day")

    total_result = await db.execute(
        text(f"""
            SELECT COUNT(*) as total, COUNT(DISTINCT endpoint) as endpoints,
                   AVG(latency_ms) as avg_latency,
                   COUNT(CASE WHEN status_code >= 400 THEN 1 END) as errors
            FROM api_usage_log
            WHERE logged_at >= NOW() - INTERVAL :interval
            {'AND user_id = :uid' if user_id else ''}
        """),
        {"interval": interval, **({"uid": user_id} if user_id else {})},
    )
    stats = dict(total_result.mappings().first())

    by_endpoint = await db.execute(
        text(f"""
            SELECT endpoint, COUNT(*) as count, AVG(latency_ms) as avg_latency
            FROM api_usage_log
            WHERE logged_at >= NOW() - INTERVAL :interval
            {'AND user_id = :uid' if user_id else ''}
            GROUP BY endpoint ORDER BY count DESC LIMIT 20
        """),
        {"interval": interval, **({"uid": user_id} if user_id else {})},
    )
    endpoints = [dict(r) for r in by_endpoint.mappings().all()]

    return {
        "period": period,
        "total": stats["total"] or 0,
        "unique_endpoints": stats["endpoints"] or 0,
        "avg_latency_ms": round(float(stats["avg_latency"] or 0), 2),
        "errors": stats["errors"] or 0,
        "top_endpoints": endpoints,
    }
