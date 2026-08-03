from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/portfolio/{share_token}")
async def view_shared_portfolio(
    share_token: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        text("""
            SELECT spv.id, spv.portfolio_id, spv.is_public, spv.expires_at, spv.created_at,
                   p.name as portfolio_name, u.username as owner_name
            FROM shared_portfolio_views spv
            JOIN portfolios p ON p.id = spv.portfolio_id
            JOIN users u ON u.id = p.ontology_object_id::uuid
            WHERE spv.share_token = :token
        """),
        {"token": share_token},
    )
    share = result.mappings().first()
    if not share:
        raise HTTPException(404, "Share not found")
    if not share["is_public"]:
        raise HTTPException(403, "This portfolio is not public")
    expires = share.get("expires_at")
    if expires and expires.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(410, "This share link has expired")

    holdings = await db.execute(
        text("""
            SELECT i.ticker, i.name, pos.quantity, pos.market_value
            FROM positions pos
            JOIN instruments i ON i.id = pos.instrument_id
            WHERE pos.portfolio_id = :pid
            ORDER BY pos.market_value DESC
            LIMIT 50
        """),
        {"pid": share["portfolio_id"]},
    )
    return {
        "portfolio_name": share["portfolio_name"],
        "owner": share["owner_name"],
        "holdings": [dict(r) for r in holdings.mappings().all()],
    }
