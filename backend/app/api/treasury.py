"""Treasury & Fixed Income API — yield curve, rates, bonds, mortgages."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.middleware.auth import get_current_user
from app.services.data.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/treasury", tags=["Treasury & Fixed Income"])


async def _get_treasury():
    prov = registry.get("treasury")
    if not prov:
        raise HTTPException(503, "Treasury provider not available. Set FRED_API_KEY.")
    return prov


@router.get("/yield-curve")
async def get_yield_curve(user: dict = Depends(get_current_user)):
    """Latest yield curve data (all maturities 1mo-30yr)."""
    prov = await _get_treasury()
    curve = await prov.fetch_yield_curve()
    return {"yield_curve": curve}


@router.get("/yields/{maturity}")
async def get_treasury_yields(
    maturity: str = "DGS10",
    days: int = Query(60, le=3650),
    user: dict = Depends(get_current_user),
):
    """Historical yield data for a specific maturity."""
    prov = await _get_treasury()
    data = await prov.fetch_yield_curve_history(maturity, days)
    return {"series_id": maturity, "data": data}


@router.get("/tips")
async def get_tips_breakevens(
    days: int = Query(60, le=3650),
    user: dict = Depends(get_current_user),
):
    """TIPS breakeven inflation rates (10-year)."""
    prov = await _get_treasury()
    data = await prov.fetch_tips_breakevens(days)
    return {"tips_breakeven": data}


@router.get("/rates")
async def get_central_bank_rates(user: dict = Depends(get_current_user)):
    """Central bank rates: EFFR, SOFR, IORB."""
    prov = await _get_treasury()
    effr = await prov.fetch_effr()
    sofr = await prov.fetch_sofr()
    iorb = await prov.fetch_iorb()
    return {"effr": effr, "sofr": sofr, "iorb": iorb}


@router.get("/mortgage")
async def get_mortgage_rates(user: dict = Depends(get_current_user)):
    """Current mortgage rates (30yr, 15yr, 5/1 ARM, conforming)."""
    prov = await _get_treasury()
    rates = await prov.fetch_mortgage_rates()
    return {"mortgage_rates": rates}


@router.get("/corporate-bonds")
async def get_corporate_bonds(user: dict = Depends(get_current_user)):
    """Corporate bond yields by rating (AAA→CCC) and credit spreads."""
    prov = registry.get("corporate_bonds")
    if not prov:
        return {"bond_yields": [], "credit_spreads": [], "note": "Set FRED_API_KEY to enable corporate bonds"}
    try:
        yields = await prov.fetch_bond_yields()
        spreads = await prov.fetch_spreads()
        return {"bond_yields": yields, "credit_spreads": spreads}
    except Exception as e:
        return {"bond_yields": [], "credit_spreads": [], "error": str(e)}
