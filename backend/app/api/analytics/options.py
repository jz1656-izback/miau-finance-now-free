from fastapi import APIRouter, Query
from typing import Optional

from app.services.data_sources import options as options_service

router = APIRouter()


@router.get("/{ticker}")
async def options_chain(
    ticker: str,
    expiration: Optional[str] = Query(None, description="Unix timestamp for specific expiration date"),
):
    return await options_service.get_options_chain(ticker, expiration=expiration)
