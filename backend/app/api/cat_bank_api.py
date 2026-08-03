"""Cat Bank API — balance, transfers, jurisdictions, tax status."""
import logging
from fastapi import APIRouter, Depends, Query

from app.middleware.auth import get_current_user
from app.services.cat_bank import get_all_balances, get_cat_balance, transfer_funds, get_cat_bank_summary
from app.services.jurisdictions import get_optimal_jurisdiction, calculate_tax_exposure, get_jurisdiction_list
from app.services.payment_router import route_payment, get_available_routes
from app.services.tax_optimizer import optimize_tax, calculate_global_tax_summary

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/catbank", tags=["Cat Bank"])


@router.get("/balance")
async def cat_balance(user: dict = Depends(get_current_user)):
    return await get_all_balances()


@router.get("/balance/{chain}/{currency}")
async def chain_balance(
    chain: str = "ethereum",
    currency: str = "USDC",
    user: dict = Depends(get_current_user),
):
    return await get_cat_balance(chain, currency)


@router.post("/transfer")
async def cat_transfer(
    from_account: str = Query("hooman"),
    to_address: str = Query(...),
    amount: float = Query(...),
    chain: str = Query("ethereum"),
    currency: str = Query("USDC"),
    user: dict = Depends(get_current_user),
):
    return await transfer_funds(from_account, to_address, amount, chain, currency)


@router.get("/jurisdictions")
async def jurisdictions(user: dict = Depends(get_current_user)):
    return {"jurisdictions": await get_jurisdiction_list()}


@router.get("/jurisdictions/optimal")
async def optimal_jurisdiction(
    purpose: str = Query("payment_routing"),
    amount: float = Query(100),
    user: dict = Depends(get_current_user),
):
    return await get_optimal_jurisdiction(amount, "eur", purpose)


@router.get("/tax/optimize")
async def tax_optimize(
    income: float = Query(9900),
    jurisdiction: str = Query("estonia"),
    user: dict = Depends(get_current_user),
):
    return await optimize_tax(income, jurisdiction)


@router.get("/tax/exposure")
async def tax_exposure(
    amount: float = Query(100),
    jurisdiction: str = Query("estonia"),
    user: dict = Depends(get_current_user),
):
    return await calculate_tax_exposure(amount, jurisdiction)


@router.get("/summary")
async def cat_bank_summary(user: dict = Depends(get_current_user)):
    return await get_cat_bank_summary()


@router.get("/route")
async def payment_route(
    amount: float = Query(99),
    currency: str = Query("eur"),
    user: dict = Depends(get_current_user),
):
    return await route_payment(amount, currency)


@router.get("/routes")
async def available_routes(
    amount: float = Query(99),
    user: dict = Depends(get_current_user),
):
    return {"routes": await get_available_routes(amount)}
