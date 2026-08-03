import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def track_event(
    db: AsyncSession,
    event: str,
    path: str,
    session_id: str,
    referrer: Optional[str] = None,
    host: Optional[str] = None,
    user_agent: Optional[str] = None,
    ip_address: Optional[str] = None,
    utm_source: Optional[str] = None,
    utm_medium: Optional[str] = None,
    utm_campaign: Optional[str] = None,
    utm_term: Optional[str] = None,
    utm_content: Optional[str] = None,
    screen_width: Optional[int] = None,
    screen_height: Optional[int] = None,
    language: Optional[str] = None,
    conversion_type: Optional[str] = None,
    conversion_value: Optional[float] = None,
    metadata: Optional[dict] = None,
    timestamp: Optional[datetime] = None,
) -> None:
    ts = timestamp or datetime.now(timezone.utc)

    if event == "page_view":
        await _track_page_view(
            db, path, referrer, user_agent, ip_address, session_id, host,
            utm_source, utm_medium, utm_campaign, utm_term, utm_content,
            screen_width, screen_height, language, ts,
        )
    elif event == "conversion":
        await _track_conversion(
            db, session_id, conversion_type or "unknown", path, referrer,
            utm_source, utm_medium, utm_campaign, conversion_value, metadata, ts,
        )


async def _track_page_view(
    db: AsyncSession, path: str, referrer: Optional[str], user_agent: Optional[str],
    ip_address: Optional[str], session_id: str, host: Optional[str],
    utm_source: Optional[str], utm_medium: Optional[str], utm_campaign: Optional[str],
    utm_term: Optional[str], utm_content: Optional[str],
    screen_width: Optional[int], screen_height: Optional[int], language: Optional[str],
    timestamp: datetime,
) -> None:
    country = _guess_country(ip_address) if ip_address else None

    query = text("""
        INSERT INTO page_views
            (path, referrer, user_agent, ip_address, country, session_id, host,
             utm_source, utm_medium, utm_campaign, utm_term, utm_content,
             screen_width, screen_height, language, timestamp)
        VALUES
            (:path, :referrer, :user_agent, :ip_address, :country, :session_id, :host,
             :utm_source, :utm_medium, :utm_campaign, :utm_term, :utm_content,
             :screen_width, :screen_height, :language, :timestamp)
    """)
    await db.execute(query, {
        "path": path, "referrer": referrer, "user_agent": user_agent,
        "ip_address": ip_address, "country": country, "session_id": session_id,
        "host": host,
        "utm_source": utm_source, "utm_medium": utm_medium,
        "utm_campaign": utm_campaign, "utm_term": utm_term, "utm_content": utm_content,
        "screen_width": screen_width, "screen_height": screen_height,
        "language": language, "timestamp": timestamp,
    })

    await _upsert_session(db, session_id, host, path, referrer, ip_address, country,
                          user_agent, utm_source, utm_medium, utm_campaign, timestamp)
    await db.commit()


async def _track_conversion(
    db: AsyncSession, session_id: str, conversion_type: str, page: Optional[str],
    referrer: Optional[str], utm_source: Optional[str], utm_medium: Optional[str],
    utm_campaign: Optional[str], value: Optional[float], metadata: Optional[dict],
    timestamp: datetime,
) -> None:
    query = text("""
        INSERT INTO conversions
            (session_id, conversion_type, page, referrer, value,
             utm_source, utm_medium, utm_campaign, metadata, timestamp)
        VALUES
            (:session_id, :conversion_type, :page, :referrer, :value,
             :utm_source, :utm_medium, :utm_campaign, :metadata, :timestamp)
    """)
    await db.execute(query, {
        "session_id": session_id, "conversion_type": conversion_type,
        "page": page, "referrer": referrer, "value": value,
        "utm_source": utm_source, "utm_medium": utm_medium,
        "utm_campaign": utm_campaign,
        "metadata": metadata or {}, "timestamp": timestamp,
    })
    await db.commit()


async def _upsert_session(
    db: AsyncSession, session_id: str, host: Optional[str], path: str,
    referrer: Optional[str], ip_address: Optional[str], country: Optional[str],
    user_agent: Optional[str], utm_source: Optional[str], utm_medium: Optional[str],
    utm_campaign: Optional[str], timestamp: datetime,
) -> None:
    browser = _parse_browser(user_agent) if user_agent else None
    os_ = _parse_os(user_agent) if user_agent else None
    device = _parse_device(user_agent) if user_agent else None

    existing = await db.execute(
        text("SELECT id, page_views FROM visitor_sessions WHERE session_id = :sid"),
        {"sid": session_id},
    )
    row = existing.fetchone()

    if row:
        await db.execute(text("""
            UPDATE visitor_sessions SET
                end_time = :ts, exit_page = :path,
                page_views = page_views + 1,
                is_bounce = FALSE,
                duration_seconds = EXTRACT(EPOCH FROM :ts - start_time)
            WHERE session_id = :sid
        """), {"ts": timestamp, "path": path, "sid": session_id})
    else:
        await db.execute(text("""
            INSERT INTO visitor_sessions
                (session_id, host, start_time, end_time, landing_page, exit_page,
                 ip_address, country, user_agent, browser, os, device_type,
                 referrer, utm_source, utm_medium, utm_campaign)
            VALUES
                (:session_id, :host, :ts, :ts, :path, :path,
                 :ip, :country, :ua, :browser, :os, :device,
                 :referrer, :us, :um, :uc)
        """), {
            "session_id": session_id, "host": host, "ts": timestamp, "path": path,
            "ip": ip_address, "country": country, "ua": user_agent,
            "browser": browser, "os": os_, "device": device,
            "referrer": referrer, "us": utm_source, "um": utm_medium, "uc": utm_campaign,
        })


def _guess_country(ip: str) -> Optional[str]:
    return None


def _parse_browser(ua: str) -> Optional[str]:
    ua_lower = ua.lower()
    if "firefox" in ua_lower and not "seamonkey" in ua_lower:
        return "Firefox"
    if "chrome" in ua_lower and "edg/" not in ua_lower and "opr/" not in ua_lower:
        return "Chrome"
    if "safari" in ua_lower and "chrome" not in ua_lower:
        return "Safari"
    if "edg/" in ua_lower:
        return "Edge"
    if "opr/" in ua_lower or "opera" in ua_lower:
        return "Opera"
    return "Other"


def _parse_os(ua: str) -> Optional[str]:
    ua_lower = ua.lower()
    if "windows" in ua_lower:
        return "Windows"
    if "mac os" in ua_lower or "macintosh" in ua_lower:
        return "macOS"
    if "linux" in ua_lower and "android" not in ua_lower:
        return "Linux"
    if "android" in ua_lower:
        return "Android"
    if "iphone" in ua_lower or "ipad" in ua_lower:
        return "iOS"
    return "Other"


def _parse_device(ua: str) -> Optional[str]:
    ua_lower = ua.lower()
    if "mobile" in ua_lower or "iphone" in ua_lower:
        return "mobile"
    if "tablet" in ua_lower or "ipad" in ua_lower:
        return "tablet"
    return "desktop"
