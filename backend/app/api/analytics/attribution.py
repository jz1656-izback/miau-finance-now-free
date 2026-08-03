"""
Portfolio attribution API endpoints.
"""

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional

from app.database import get_db
from app.services.analytics import attribution as attribution_service

router = APIRouter()


@router.get("/{portfolio_id}")
async def get_portfolio_attribution(
    portfolio_id: UUID = Path(..., description="Portfolio ID"),
    benchmark: str = Query("SPY", description="Benchmark ticker for attribution comparison"),
    period: str = Query("1y", description="Return period (1mo, 3mo, 6mo, 1y, 2y, 5y)"),
    db: AsyncSession = Depends(get_db),
):
    """Full attribution report for a portfolio (sector + security + factor)."""
    return await attribution_service.get_full_attribution_report(db, portfolio_id, benchmark, 3, period)


@router.get("/{portfolio_id}/sector")
async def get_sector_attribution(
    portfolio_id: UUID = Path(..., description="Portfolio ID"),
    benchmark: str = Query("SPY", description="Benchmark ticker"),
    period: str = Query("1y", description="Return period"),
    db: AsyncSession = Depends(get_db),
):
    """Brinson-style sector attribution: allocation + selection effects."""
    return await attribution_service.get_sector_attribution(db, portfolio_id, benchmark, period)


@router.get("/{portfolio_id}/security")
async def get_security_attribution(
    portfolio_id: UUID = Path(..., description="Portfolio ID"),
    period: str = Query("1y", description="Return period"),
    db: AsyncSession = Depends(get_db),
):
    """Per-security contribution to portfolio return."""
    return await attribution_service.get_security_attribution(db, portfolio_id, period)


@router.get("/{portfolio_id}/factor")
async def get_factor_attribution(
    portfolio_id: UUID = Path(..., description="Portfolio ID"),
    model: int = Query(3, ge=3, le=5, description="Fama-French model (3 or 5 factor)"),
    include_momentum: bool = Query(False, description="Include momentum factor"),
    period: str = Query("1y", description="Return period"),
    db: AsyncSession = Depends(get_db),
):
    """Factor attribution using Fama-French models."""
    return await attribution_service.get_factor_attribution(
        db, portfolio_id, model, include_momentum, period,
    )
