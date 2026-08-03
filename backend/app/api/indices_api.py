"""Index API — global market indices, quotes, performance."""
import logging
from fastapi import APIRouter, Depends, HTTPException

from app.middleware.auth import get_current_user
from app.services.data.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/indices", tags=["Indices"])


async def _get_idx():
    prov = registry.get("indices")
    if not prov:
        raise HTTPException(503, "Index provider not available")
    return prov


@router.get("/list")
async def list_indices(user: dict = Depends(get_current_user)):
    prov = await _get_idx()
    return {"indices": await prov.fetch_index_list()}


@router.get("/quote/{ticker}")
async def index_quote(ticker: str, user: dict = Depends(get_current_user)):
    prov = await _get_idx()
    return await prov.fetch_index_quote(ticker)


@router.get("/all")
async def all_indices(user: dict = Depends(get_current_user)):
    prov = await _get_idx()
    indices = await prov.fetch_all_indices()
    return {"indices": indices, "count": len(indices)}
