from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.middleware.rbac import get_current_user_db

router = APIRouter(prefix="/paper/trades", tags=["Paper Trading"])


@router.get("")
async def list_paper_trades(
    portfolio_id: UUID,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT pt.*, i.ticker, i.name as instrument_name
            FROM paper_trades pt
            JOIN instruments i ON i.id = pt.instrument_id
            WHERE pt.paper_portfolio_id = :pid
            ORDER BY pt.executed_at DESC
            LIMIT :limit OFFSET :offset
        """),
        {"pid": portfolio_id, "limit": limit, "offset": offset},
    )
    return {"trades": [dict(r) for r in result.mappings().all()], "total": len(result.mappings().all())}


@router.get("/{trade_id}")
async def get_paper_trade(
    trade_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT pt.*, i.ticker, i.name as instrument_name
            FROM paper_trades pt
            JOIN instruments i ON i.id = pt.instrument_id
            WHERE pt.id = :tid
        """),
        {"tid": trade_id},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "Trade not found")
    return dict(row)
