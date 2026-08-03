"""Commodities API — spot prices, energy, agricultural, tuna index."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query

from app.middleware.auth import get_current_user
from app.services.data.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/commodities", tags=["Commodities"])


async def _get_prov():
    prov = registry.get("commodities")
    if not prov:
        raise HTTPException(503, "Commodities provider not available")
    return prov


@router.get("/all")
async def all_commodities(user: dict = Depends(get_current_user)):
    prov = await _get_prov()
    return {"commodities": await prov.fetch_all_commodities()}


@router.get("/{ticker}")
async def commodity_quote(ticker: str, user: dict = Depends(get_current_user)):
    prov = await _get_prov()
    return await prov.fetch_commodity(ticker)


@router.get("/category/{category}")
async def commodities_by_category(category: str, user: dict = Depends(get_current_user)):
    prov = await _get_prov()
    return {"commodities": await prov.fetch_by_category(category)}


@router.get("/tuna/price")
async def tuna_price(user: dict = Depends(get_current_user)):
    prov = await _get_prov()
    return await prov.fetch_tuna_price()


@router.get("/tuna/index")
async def cat_food_index(user: dict = Depends(get_current_user)):
    prov = await _get_prov()
    return {"cat_food_index": await prov.fetch_cat_food_index()}
