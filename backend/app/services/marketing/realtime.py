from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def get_realtime(db: AsyncSession) -> dict:
    rows = await db.execute(text("""
        WITH last_min AS (
            SELECT count(*) AS cnt FROM page_views WHERE timestamp > NOW() - INTERVAL '1 minute'
        ), last_5 AS (
            SELECT count(*) AS cnt FROM page_views WHERE timestamp > NOW() - INTERVAL '5 minutes'
        ), last_hour AS (
            SELECT count(*) AS cnt FROM conversions WHERE timestamp > NOW() - INTERVAL '1 hour'
        ), recent AS (
            SELECT id, 'page_view' AS event, path, timestamp::text, session_id, host, NULL::text AS conversion_type
            FROM page_views WHERE timestamp > NOW() - INTERVAL '2 minutes'
            UNION ALL
            SELECT c.id, 'conversion' AS event, p.path, c.timestamp::text, p.session_id, p.host, c.conversion_type
            FROM conversions c LEFT JOIN page_views p ON p.session_id = c.session_id
            WHERE c.timestamp > NOW() - INTERVAL '2 minutes'
            ORDER BY timestamp DESC LIMIT 30
        ), hourly AS (
            SELECT to_char(date_trunc('hour', timestamp), 'HH24:00') AS hour,
                   count(*) AS page_views,
                   count(DISTINCT session_id) AS visitors
            FROM page_views WHERE timestamp > NOW() - INTERVAL '24 hours'
            GROUP BY date_trunc('hour', timestamp) ORDER BY hour
        )
        SELECT (SELECT cnt FROM last_min) AS last_min,
               (SELECT cnt FROM last_5) AS last_5,
               (SELECT cnt FROM last_hour) AS last_hour,
               (SELECT count(*) FROM visitor_sessions WHERE end_time IS NULL) AS active,
               (SELECT json_agg(row_to_json(r)) FROM recent r) AS events,
               (SELECT json_agg(row_to_json(h)) FROM hourly h) AS breakdown
    """))
    row = rows.mappings().first()
    if not row:
        return {"active_sessions": 0, "page_views_last_minute": 0, "page_views_last_5_minutes": 0,
                "conversions_last_hour": 0, "top_page_current": None, "recent_events": [], "hourly_breakdown": []}
    return {
        "active_sessions": row["active"],
        "page_views_last_minute": row["last_min"],
        "page_views_last_5_minutes": row["last_5"],
        "conversions_last_hour": row["last_hour"],
        "top_page_current": None,
        "recent_events": row["events"] or [],
        "hourly_breakdown": row["breakdown"] or [],
    }


async def get_geo(db: AsyncSession, period: int) -> list[dict]:
    rows = await db.execute(text("""
        SELECT COALESCE(NULLIF(country, ''), 'Unknown') AS country,
               count(*) AS page_views,
               count(DISTINCT session_id) AS visitors
        FROM page_views WHERE timestamp > NOW() - INTERVAL '1 day' * :period
        GROUP BY country
        ORDER BY visitors DESC
    """), {"period": period})
    return [dict(r._mapping) for r in rows]


async def get_devices(db: AsyncSession, period: int) -> list[dict]:
    rows = await db.execute(text("""
        SELECT COALESCE(NULLIF(vs.device_type, ''), 'desktop') AS device_type,
               count(*) AS page_views,
               count(DISTINCT pv.session_id) AS visitors
        FROM page_views pv
        LEFT JOIN visitor_sessions vs ON vs.session_id = pv.session_id
        WHERE pv.timestamp > NOW() - INTERVAL '1 day' * :period
        GROUP BY vs.device_type ORDER BY visitors DESC
    """), {"period": period})
    result = [dict(r._mapping) for r in rows]
    total = sum(r["visitors"] for r in result) or 1
    for r in result:
        r["percentage"] = round(r["visitors"] / total * 100, 1)
    return result


async def get_compare(db: AsyncSession, period: int) -> dict:
    cur = await db.execute(text("""
        SELECT count(DISTINCT pv.session_id) AS visitors,
               count(*) AS page_views,
               count(*) AS conversions,
               COALESCE(avg(pv.duration_seconds), 0) AS avg_session_duration
        FROM page_views pv WHERE pv.timestamp > NOW() - INTERVAL '1 day' * :period
    """), {"period": period})
    prev = await db.execute(text("""
        SELECT count(DISTINCT pv.session_id) AS visitors,
               count(*) AS page_views,
               count(*) AS conversions,
               COALESCE(avg(pv.duration_seconds), 0) AS avg_session_duration
        FROM page_views pv
        WHERE pv.timestamp >= NOW() - INTERVAL '1 day' * :period * 2
          AND pv.timestamp < NOW() - INTERVAL '1 day' * :period
    """), {"period": period})
    c = dict(cur.mappings().first() or {})
    p = dict(prev.mappings().first() or {})
    return {
        "current": {"visitors": c.get("visitors", 0), "page_views": c.get("page_views", 0),
                     "conversions": c.get("conversions", 0), "bounce_rate": 0, "avg_session_duration": c.get("avg_session_duration", 0)},
        "previous": {"visitors": p.get("visitors", 0), "page_views": p.get("page_views", 0),
                     "conversions": p.get("conversions", 0), "bounce_rate": 0, "avg_session_duration": p.get("avg_session_duration", 0)},
    }
