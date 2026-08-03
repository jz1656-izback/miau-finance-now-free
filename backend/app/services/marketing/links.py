import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def create_link(db: AsyncSession, url: str, slug: str | None = None,
                      title: str | None = None, campaign: str | None = None,
                      source: str | None = None, medium: str | None = None,
                      created_by: str | None = None) -> dict:
    if not slug:
        slug = secrets.token_urlsafe(6)
    base = "https://miau.finance"
    short_url = f"{base}/go/{slug}"
    row = await db.execute(text("""
        INSERT INTO tracked_links (url, slug, short_url, title, campaign, source, medium, created_by)
        VALUES (:url, :slug, :short_url, :title, :campaign, :source, :medium, :created_by)
        RETURNING id, url, slug, short_url, title, campaign, source, medium, total_clicks, unique_visitors, created_at, created_by
    """), {"url": url, "slug": slug, "short_url": short_url, "title": title,
           "campaign": campaign, "source": source, "medium": medium, "created_by": created_by})
    await db.commit()
    return dict(row.mappings().first())


async def list_links(db: AsyncSession) -> list[dict]:
    rows = await db.execute(text("""
        SELECT id, url, slug, short_url, title, campaign, source, medium,
               total_clicks, unique_visitors, created_at, created_by
        FROM tracked_links ORDER BY created_at DESC
    """))
    return [dict(r._mapping) for r in rows]


async def get_link_clicks(db: AsyncSession, link_id: str, period: int) -> list[dict]:
    rows = await db.execute(text("""
        SELECT id, link_id, ip_address, user_agent, country, timestamp
        FROM link_clicks
        WHERE link_id = :link_id AND timestamp > NOW() - INTERVAL '1 day' * :period
        ORDER BY timestamp DESC
    """), {"link_id": link_id, "period": period})
    return [dict(r._mapping) for r in rows]
