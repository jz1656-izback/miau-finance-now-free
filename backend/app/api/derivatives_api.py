"""Derivatives API — futures, options."""
import logging
from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.services.data.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/derivatives", tags=["Derivatives"])


async def _get_futures():
    prov = registry.get("futures")
    if not prov:
        raise HTTPException(503, "Futures provider not available")
    return prov


@router.get("/futures")
async def all_futures(user: dict = Depends(get_current_user)):
    prov = await _get_futures()
    return {"futures": await prov.fetch_all_futures()}


@router.get("/futures/{ticker}")
async def future_quote(ticker: str, user: dict = Depends(get_current_user)):
    prov = await _get_futures()
    return await prov.fetch_future(ticker)


@router.get("/futures/category/{category}")
async def futures_by_category(category: str, user: dict = Depends(get_current_user)):
    prov = await _get_futures()
    return {"futures": await prov.fetch_by_category(category)}
