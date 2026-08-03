import logging
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.currency_service import (
    convert_amount,
    get_currency_info,
    list_currencies,
    SUPPORTED_CURRENCIES,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/currencies", tags=["Currencies"])


@router.get("")
async def get_currencies(db: AsyncSession = Depends(get_db)):
    return await list_currencies(db)


@router.get("/convert")
async def convert_currency(
    amount: float = Query(..., gt=0),
    from_: str = Query(..., alias="from", min_length=3, max_length=5),
    to: str = Query(..., min_length=3, max_length=5),
    db: AsyncSession = Depends(get_db),
):
    from_code = from_.upper()
    to_code = to.upper()

    if from_code not in SUPPORTED_CURRENCIES:
        raise HTTPException(400, f"Unsupported currency: {from_code}")
    if to_code not in SUPPORTED_CURRENCIES:
        raise HTTPException(400, f"Unsupported currency: {to_code}")

    result = await convert_amount(db, Decimal(str(amount)), from_code, to_code)
    if result is None:
        raise HTTPException(502, "FX rate unavailable")

    return {
        "from": from_code,
        "to": to_code,
        "amount": amount,
        "result": float(result),
        "rate": float(result) / amount if amount else 0,
    }


@router.get("/{code}")
async def get_currency(code: str, db: AsyncSession = Depends(get_db)):
    info = await get_currency_info(code.upper())
    if not info:
        raise HTTPException(404, f"Currency not found: {code}")
    return info
