from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from app.database import get_db
from app.services import analytics_service
from app.services.analytics.pnl import compute_fx_pnl, get_pnl_with_fx_breakdown

router = APIRouter()


@router.get("/summary")
async def get_summary(db: AsyncSession = Depends(get_db)):
    return await analytics_service.get_summary_dashboard(db)


@router.get("/portfolios/{portfolio_id}")
async def get_portfolio_analytics(portfolio_id: UUID, db: AsyncSession = Depends(get_db)):
    summary = await analytics_service.get_portfolio_summary(db, portfolio_id)
    if not summary:
        raise HTTPException(404, "Portfolio not found")
    pnl = await analytics_service.get_pnl_timeseries(db, portfolio_id)
    risk = await analytics_service.get_portfolio_risk_metrics(db, portfolio_id)
    return {"summary": summary, "pnl_timeseries": pnl, "risk_metrics": risk}


@router.get("/instruments/{instrument_id}/performance")
async def get_instrument_performance(instrument_id: UUID, db: AsyncSession = Depends(get_db)):
    return await analytics_service.get_instrument_performance(db, instrument_id)


@router.get("/pnl/timeseries")
async def get_pnl_timeseries(
    portfolio_id: Optional[UUID] = None,
    days: int = Query(30, ge=1, le=3650),
    db: AsyncSession = Depends(get_db),
):
    return await analytics_service.get_pnl_timeseries(db, portfolio_id, days)


@router.get("/portfolios/{portfolio_id}/risk")
async def get_portfolio_risk(portfolio_id: UUID, db: AsyncSession = Depends(get_db)):
    return await analytics_service.get_portfolio_risk_metrics(db, portfolio_id)


@router.get("/portfolios/{portfolio_id}/fx-pnl")
async def get_portfolio_fx_pnl(
    portfolio_id: UUID,
    days: int = Query(30, ge=1, le=3650),
    db: AsyncSession = Depends(get_db),
):
    return await get_pnl_with_fx_breakdown(db, portfolio_id, days)
