from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from app.database import get_db
from app.models import Instrument, MarketData

router = APIRouter()


@router.get("")
async def list_instruments(
    type: Optional[str] = Query(None, pattern=r"^[\w\-]{0,50}$", max_length=50),
    sector: Optional[str] = Query(None, pattern=r"^[\w\s\-]{0,50}$", max_length=50),
    exchange: Optional[str] = Query(None, pattern=r"^[A-Z]{0,10}$", max_length=10),
    search: Optional[str] = Query(None, pattern=r"^[\w\s\-_.]{0,200}$", max_length=200),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Instrument)
    if type:
        stmt = stmt.where(Instrument.instrument_type == type)
    if sector:
        stmt = stmt.where(Instrument.sector == sector)
    if exchange:
        stmt = stmt.where(Instrument.exchange == exchange)
    if search:
        pattern = f"%{search}%"
        stmt = stmt.where(
            Instrument.ticker.ilike(pattern) |
            Instrument.name.ilike(pattern) |
            Instrument.isin.ilike(pattern)
        )
    stmt = stmt.order_by(Instrument.ticker).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return [row.Instrument.to_dict() for row in result.unique().all()]


@router.get("/{instrument_id}")
async def get_instrument(instrument_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Instrument).where(Instrument.id == instrument_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(404, f"Instrument {instrument_id} not found")
    return row.to_dict()


@router.get("/{instrument_id}/market-data")
async def get_market_data(
    instrument_id: UUID,
    from_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$", max_length=10),
    to_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$", max_length=10),
    limit: int = Query(500, ge=1, le=5000),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(MarketData).where(MarketData.instrument_id == instrument_id)
    if from_date:
        stmt = stmt.where(MarketData.date >= from_date)
    if to_date:
        stmt = stmt.where(MarketData.date <= to_date)
    stmt = stmt.order_by(MarketData.date.desc()).limit(limit)
    result = await db.execute(stmt)
    return [row.MarketData.to_dict() for row in result.unique().all()]


@router.get("/sectors/list")
async def list_sectors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Instrument.sector).distinct().where(Instrument.sector.isnot(None)).order_by(Instrument.sector)
    )
    return [row.sector for row in result.fetchall()]


@router.get("/types/list")
async def list_instrument_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Instrument.instrument_type).distinct().order_by(Instrument.instrument_type)
    )
    return [row.instrument_type for row in result.fetchall()]