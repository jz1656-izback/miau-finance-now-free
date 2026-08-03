import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def get_overview(db: AsyncSession, period_days: int = 30) -> dict:
    since = datetime.now(timezone.utc) - timedelta(days=period_days)
    result = await db.execute(text("""
        SELECT
            COUNT(DISTINCT session_id) AS total_visitors,
            COUNT(*) AS total_page_views,
            COALESCE(
                (COUNT(*) FILTER (WHERE is_bounce = TRUE))::float /
                NULLIF(COUNT(*), 0) * 100, 0
            ) AS bounce_rate,
            COALESCE(
                AVG(duration_seconds) FILTER (WHERE duration_seconds IS NOT NULL), 0
            ) AS avg_session_duration,
            COALESCE(
                (SELECT COUNT(*) FROM conversions WHERE timestamp >= :since)::float /
                NULLIF((SELECT COUNT(DISTINCT session_id) FROM page_views
                        WHERE timestamp >= :since), 0) * 100, 0
            ) AS conversion_rate,
            (SELECT COUNT(DISTINCT session_id) FROM page_views
             WHERE timestamp >= :since2) AS active_sessions,
            (SELECT COUNT(*) FROM conversions WHERE timestamp >= :since) AS total_conversions
        FROM visitor_sessions
        WHERE start_time >= :since
    """), {"since": since, "since2": since - timedelta(minutes=30)})
    row = result.fetchone()
    return {
        "total_visitors": row[0],
        "total_page_views": row[1],
        "bounce_rate": round(float(row[2]), 1),
        "avg_session_duration": round(float(row[3]), 1),
        "conversion_rate": round(float(row[4]), 2),
        "active_sessions": row[5],
        "total_conversions": row[6],
    }


async def get_pages(db: AsyncSession, period_days: int = 30, limit: int = 50) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=period_days)
    result = await db.execute(text("""
        SELECT
            path,
            COUNT(*) AS views,
            COUNT(DISTINCT session_id) AS unique_views,
            COALESCE(AVG(duration_seconds), 0) AS avg_time,
            COUNT(*) FILTER (WHERE duration_seconds < 5 OR duration_seconds IS NULL)::float
                / NULLIF(COUNT(*), 0) * 100 AS bounce_rate
        FROM page_views
        WHERE timestamp >= :since
        GROUP BY path
        ORDER BY views DESC
        LIMIT :limit
    """), {"since": since, "limit": limit})
    return [
        {
            "path": r[0], "views": r[1], "unique_views": r[2],
            "avg_time_on_page": round(float(r[3]), 1),
            "bounce_rate": round(float(r[4]), 1),
        }
        for r in result.fetchall()
    ]


async def get_referrers(db: AsyncSession, period_days: int = 30) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=period_days)
    result = await db.execute(text("""
        SELECT
            source,
            visitors,
            page_views,
            bounce_rate,
            conversions
        FROM (
            SELECT
                COALESCE(NULLIF(pv.referrer, ''), 'direct') AS source,
                COUNT(DISTINCT pv.session_id) AS visitors,
                COUNT(*) AS page_views,
                COALESCE(
                    COUNT(*) FILTER (WHERE vs.is_bounce = TRUE)::float /
                    NULLIF(COUNT(*), 0) * 100, 0
                ) AS bounce_rate
            FROM page_views pv
            JOIN visitor_sessions vs ON vs.session_id = pv.session_id
            WHERE pv.timestamp >= :since
            GROUP BY COALESCE(NULLIF(pv.referrer, ''), 'direct')
        ) sub
        LEFT JOIN LATERAL (
            SELECT COUNT(*) AS conversions
            FROM conversions c
            WHERE c.timestamp >= :since
              AND COALESCE(NULLIF(c.referrer, ''), 'direct') = sub.source
        ) conv ON TRUE
        ORDER BY page_views DESC
    """), {"since": since})
    return [
        {
            "source": r[0], "visitors": r[1], "page_views": r[2],
            "bounce_rate": round(float(r[3]), 1),
            "conversions": r[4],
        }
        for r in result.fetchall()
    ]


async def get_public_campaigns(db: AsyncSession, period_days: int = 30) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=period_days)
    result = await db.execute(text("""
        SELECT campaign, visitors, page_views, conversions
        FROM (
            SELECT COALESCE(utm_campaign, '(none)') AS campaign,
                   COUNT(DISTINCT session_id) AS visitors,
                   COUNT(*) AS page_views
            FROM page_views
            WHERE timestamp >= :since AND utm_campaign IS NOT NULL
            GROUP BY COALESCE(utm_campaign, '(none)')
        ) pv
        LEFT JOIN LATERAL (
            SELECT COUNT(*) AS conversions
            FROM conversions c
            WHERE c.timestamp >= :since AND COALESCE(c.utm_campaign, '') = pv.campaign
        ) conv ON TRUE
        ORDER BY visitors DESC
    """), {"since": since})
    return [
        {"campaign": r[0], "visitors": r[1], "page_views": r[2],
         "conversions": r[3],
         "conversion_rate": round(r[3] / r[1] * 100, 2) if r[1] else 0}
        for r in result.fetchall()
    ]


async def get_campaigns(db: AsyncSession, period_days: int = 30) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=period_days)
    result = await db.execute(text("""
        SELECT
            campaign, source, medium, visitors, page_views, conversions
        FROM (
            SELECT
                COALESCE(utm_campaign, '(none)') AS campaign,
                COALESCE(utm_source, 'direct') AS source,
                COALESCE(utm_medium, 'none') AS medium,
                COUNT(DISTINCT session_id) AS visitors,
                COUNT(*) AS page_views
            FROM page_views
            WHERE timestamp >= :since AND utm_campaign IS NOT NULL
            GROUP BY COALESCE(utm_campaign, '(none)'), COALESCE(utm_source, 'direct'), COALESCE(utm_medium, 'none')
        ) pv
        LEFT JOIN LATERAL (
            SELECT COUNT(*) AS conversions
            FROM conversions c
            WHERE c.timestamp >= :since
              AND COALESCE(c.utm_campaign, '') = pv.campaign
        ) conv ON TRUE
        ORDER BY pv.visitors DESC
    """), {"since": since})
    return [
        {
            "campaign": r[0], "source": r[1], "medium": r[2],
            "visitors": r[3], "page_views": r[4], "conversions": r[5],
            "conversion_rate": round(r[5] / r[3] * 100, 2) if r[3] else 0,
            "revenue": 0.0,
        }
        for r in result.fetchall()
    ]


async def get_trends(db: AsyncSession, period_days: int = 30) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=period_days)
    result = await db.execute(text("""
        SELECT
            d,
            visitors,
            page_views,
            COALESCE((SELECT COUNT(*) FROM conversions c WHERE DATE(c.timestamp) = d), 0) AS conversions
        FROM (
            SELECT
                DATE(pv.timestamp) AS d,
                COUNT(DISTINCT pv.session_id) AS visitors,
                COUNT(*) AS page_views
            FROM page_views pv
            WHERE pv.timestamp >= :since
            GROUP BY DATE(pv.timestamp)
        ) sub
        ORDER BY d
    """), {"since": since})
    return [
        {"date": str(r[0]), "visitors": r[1], "page_views": r[2], "conversions": r[3]}
        for r in result.fetchall()
    ]


async def get_conversions(db: AsyncSession, period_days: int = 30, limit: int = 100) -> list[dict]:
    since = datetime.now(timezone.utc) - timedelta(days=period_days)
    result = await db.execute(text("""
        SELECT id, conversion_type, page, referrer, value,
               utm_source, utm_medium, utm_campaign, timestamp
        FROM conversions
        WHERE timestamp >= :since
        ORDER BY timestamp DESC
        LIMIT :limit
    """), {"since": since, "limit": limit})
    return [
        {
            "id": str(r[0]), "conversion_type": r[1], "page": r[2],
            "referrer": r[3], "value": float(r[4]) if r[4] else None,
            "utm_source": r[5], "utm_medium": r[6], "utm_campaign": r[7],
            "timestamp": r[8].isoformat() if r[8] else None,
        }
        for r in result.fetchall()
    ]
