from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.middleware.auth import get_current_user
from app.services.analytics.valuation import (
    build_dcf,
    calculate_wacc,
    comparable_analysis,
    lbo_model,
    sensitivity_table,
    lbo_sensitivity_table,
    football_field,
    accretion_dilution,
)

router = APIRouter(prefix="/valuation", tags=["Valuation"])


@router.get("/wacc/{ticker}")
async def api_wacc(
    ticker: str,
    user: dict = Depends(get_current_user),
):
    return await calculate_wacc(ticker)


@router.get("/dcf/{ticker}")
async def api_dcf(
    ticker: str,
    growth: float = Query(0.05, ge=-0.5, le=0.5, description="Annual FCF growth rate"),
    terminal_growth: float = Query(0.025, ge=0.0, le=0.1, description="Terminal/perpetuity growth rate"),
    years: int = Query(5, ge=3, le=10, description="Projection years"),
    exit_multiple: Optional[float] = Query(None, ge=0, le=100, description="Exit multiple (disables Gordon Growth)"),
    user: dict = Depends(get_current_user),
):
    return await build_dcf(
        ticker,
        growth_rate=growth,
        terminal_growth=terminal_growth,
        projection_years=years,
        exit_multiple=exit_multiple,
    )


@router.get("/comps/{ticker}")
async def api_comps(
    ticker: str,
    user: dict = Depends(get_current_user),
):
    return await comparable_analysis(ticker)


@router.get("/lbo/{ticker}")
async def api_lbo(
    ticker: str,
    debt: float = Query(0.60, ge=0.3, le=0.9, description="Debt percentage (30-90%)"),
    exit_year: int = Query(5, ge=3, le=10),
    exit_multiple: float = Query(10.0, ge=1, le=50),
    user: dict = Depends(get_current_user),
):
    return await lbo_model(
        ticker,
        debt_pct=debt,
        exit_year=exit_year,
        exit_multiple=exit_multiple,
    )


@router.get("/sensitivity/{ticker}")
async def api_sensitivity(
    ticker: str,
    type: str = Query("wacc", pattern="^(wacc|lbo)$"),
    user: dict = Depends(get_current_user),
):
    if type == "lbo":
        return await lbo_sensitivity_table(ticker)
    return await sensitivity_table(ticker)


@router.get("/football/{ticker}")
async def api_football_field(
    ticker: str,
    user: dict = Depends(get_current_user),
):
    return await football_field(ticker)


@router.get("/accretion/{acquirer}/{target}")
async def api_accretion(
    acquirer: str,
    target: str,
    deal_value: Optional[float] = Query(None, description="Override deal value"),
    cash_pct: float = Query(0.50, ge=0.0, le=1.0),
    synergies: float = Query(0.05, ge=0.0, le=0.50, description="Expected cost/revenue synergies"),
    user: dict = Depends(get_current_user),
):
    return await accretion_dilution(
        acquirer, target,
        deal_value=deal_value,
        cash_pct=cash_pct,
        stock_pct=1.0 - cash_pct,
        synergies_pct=synergies,
    )
