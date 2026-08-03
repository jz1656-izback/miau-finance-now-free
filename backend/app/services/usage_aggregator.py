"""Usage aggregation cron job — runs daily via Airflow or scheduler.

Aggregates api_usage_log entries into daily/weekly/monthly rollups
for the developer dashboard and billing system.
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy import text
from app.database import async_session

logger = logging.getLogger(__name__)

INTERVALS = {
    "daily": "1 day",
    "weekly": "7 days",
    "monthly": "30 days",
}


async def aggregate_usage(period: str = "daily") -> dict:
    interval = INTERVALS.get(period, "1 day")
    async with async_session() as db:
        result = await db.execute(
            text(f"""
                INSERT INTO usage_rollups (period, interval_type, total_requests, unique_endpoints, avg_latency_ms, error_count, recorded_at)
                SELECT
                    DATE(NOW()) as period,
                    :period as interval_type,
                    COUNT(*) as total_requests,
                    COUNT(DISTINCT endpoint) as unique_endpoints,
                    COALESCE(AVG(latency_ms), 0) as avg_latency_ms,
                    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count,
                    NOW() as recorded_at
                FROM api_usage_log
                WHERE logged_at >= NOW() - INTERVAL :interval
            """),
            {"period": period, "interval": interval},
        )
        await db.commit()
        logger.info(f"Usage aggregated for {period}: {result.rowcount} rows")
        return {"period": period, "aggregated": True}


async def aggregate_all_periods():
    for period in ["daily", "weekly", "monthly"]:
        await aggregate_usage(period)
    logger.info("All usage periods aggregated")
