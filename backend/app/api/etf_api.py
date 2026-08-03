"""ETF API — quotes, sectors, top ETFs, screener."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.services.data.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/etf", tags=["ETF"])


async def _get_etf():
    prov = registry.get("etf")
    if not prov:
        raise HTTPException(503, "ETF provider not available")
    return prov


@router.get("/list")
async def list_etfs(user: dict = Depends(get_current_user)):
    prov = await _get_etf()
    return {"etfs": await prov.fetch_etf_list()}


@router.get("/quote/{ticker}")
async def etf_quote(ticker: str, user: dict = Depends(get_current_user)):
    prov = await _get_etf()
    return await prov.fetch_etf_quote(ticker)


@router.get("/sectors")
async def sector_etfs(user: dict = Depends(get_current_user)):
    prov = await _get_etf()
    return await prov.fetch_sector_performance()


@router.get("/top")
async def top_etfs(limit: int = Query(10, le=50), user: dict = Depends(get_current_user)):
    prov = await _get_etf()
    etfs = await prov.fetch_top_etfs(limit)
    return {"top_etfs": etfs}
