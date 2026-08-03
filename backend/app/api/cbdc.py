import logging
from fastapi import APIRouter, Depends, Query
from app.middleware.auth import get_current_user
from app.services.cbdc import euro, yuan, dollar, yen, pound
from app.services.cbdc import cross_settlement, interest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cbdc", tags=["CBDC"])

CURRENCIES = {"deur": euro, "ecny": yuan, "dusd": dollar, "dcjpy": yen, "gbp+": pound}


@router.get("/currencies")
async def list_cbdcs(user: dict = Depends(get_current_user)):
    return await cross_settlement.list_cbdcs()


@router.get("/{code}/info")
async def cbdc_info(code: str, user: dict = Depends(get_current_user)):
    mod = CURRENCIES.get(code.lower())
    if not mod:
        return {"error": f"CBDC '{code}' not supported"}
    return await mod.get_info()


@router.get("/{code}/rates")
async def cbdc_rates(code: str, user: dict = Depends(get_current_user)):
    import importlib
    try:
        mod = importlib.import_module(f"app.services.cbdc.{ {'deur':'euro','ecny':'yuan','dusd':'dollar','dcjpy':'yen','gbp+':'pound'}[code.lower()] }")
        return await mod.get_rates()
    except (KeyError, ModuleNotFoundError):
        return {"error": f"CBDC '{code}' not supported"}


@router.post("/transfer")
async def cbdc_transfer(
    code: str = Query(..., description="CBDC code"),
    amount: float = Query(...),
    to_currency: str = Query("USD"),
    user: dict = Depends(get_current_user),
):
    mod = CURRENCIES.get(code.lower())
    if not mod:
        return {"error": f"CBDC '{code}' not supported"}
    return await mod.simulate_transfer(amount, to_currency)


@router.post("/settle")
async def cbdc_settle(
    from_cbdc: str = Query("DEUR"),
    to_cbdc: str = Query("DUSD"),
    amount: float = Query(10000),
    user: dict = Depends(get_current_user),
):
    return await cross_settlement.settle(from_cbdc, to_cbdc, amount)


@router.get("/settlement/corridors")
async def settlement_corridors(user: dict = Depends(get_current_user)):
    return await cross_settlement.list_cbdcs()


@router.get("/interest/rates")
async def interest_rates(user: dict = Depends(get_current_user)):
    return await interest.get_current_rates()


@router.get("/interest/{code}")
async def interest_rate_detail(code: str, user: dict = Depends(get_current_user)):
    return await interest.get_rate(code)


@router.get("/interest/{code}/history")
async def interest_rate_history(code: str, user: dict = Depends(get_current_user)):
    return await interest.get_rate_history(code)


@router.get("/interest/{code}/project")
async def interest_project(
    code: str,
    balance: float = Query(10000),
    days: int = Query(365),
    user: dict = Depends(get_current_user),
):
    return await interest.project_interest(balance, code, days)
