from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from app.database import get_db

router = APIRouter()


@router.get("")
async def list_trades(
    status: Optional[str] = Query(None, pattern=r"^[\w\-]{0,50}$", max_length=50),
    portfolio_id: Optional[UUID] = None,
    instrument_id: Optional[UUID] = None,
    trader: Optional[str] = Query(None, pattern=r"^[\w\s\-_.]{0,100}$", max_length=100),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    conditions = []
    params = {"limit": limit, "offset": offset}
    if status:
        conditions.append("t.status = :status")
        params["status"] = status
    if portfolio_id:
        conditions.append("t.portfolio_id = :pid")
        params["pid"] = portfolio_id
    if instrument_id:
        conditions.append("t.instrument_id = :iid")
        params["iid"] = instrument_id
    if trader:
        conditions.append("t.trader ILIKE :trader")
        params["trader"] = f"%{trader}%"

    where = " AND ".join(conditions) if conditions else "TRUE"
    result = await db.execute(
        text(f"""
            SELECT t.*, i.ticker, i.name as instrument_name,
                   p.name as portfolio_name
            FROM trades t
            JOIN instruments i ON t.instrument_id = i.id
            LEFT JOIN portfolios p ON t.portfolio_id = p.id
            WHERE {where}
            ORDER BY t.trade_date DESC
            LIMIT :limit OFFSET :offset
        """),
        params,
    )
    return [dict(row) for row in result.mappings().all()]


@router.get("/{trade_id}")
async def get_trade(trade_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT t.*, i.ticker, i.name as instrument_name,
                   p.name as portfolio_name, cp.short_name as counterparty_name
            FROM trades t
            JOIN instruments i ON t.instrument_id = i.id
            LEFT JOIN portfolios p ON t.portfolio_id = p.id
            LEFT JOIN counterparties cp ON t.counterparty_id = cp.id
            WHERE t.id = :id
        """),
        {"id": trade_id},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, detail=f"Trade with ID {trade_id} not found")
    return dict(row)
