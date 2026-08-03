import logging
from fastapi import APIRouter, Depends, Query
from app.middleware.auth import get_current_user
from app.services.defi.protocols import uniswap, aave, curve, lido, yearn, maker

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/defi/protocols", tags=["DeFi Protocols"])


@router.get("/uniswap/pool")
async def uniswap_pool_info(
    pool: str = Query("0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"),
    chain: str = "ethereum",
    user: dict = Depends(get_current_user),
):
    return await uniswap.get_pool_info(pool, chain)


@router.get("/uniswap/swap")
async def uniswap_simulate(
    token_in: str = Query("WETH"),
    token_out: str = Query("USDC"),
    amount: float = Query(1.0),
    chain: str = "ethereum",
    user: dict = Depends(get_current_user),
):
    return await uniswap.simulate_swap(token_in, token_out, amount, chain)


@router.get("/aave/reserve")
async def aave_reserve(
    asset: str = Query("USDC"),
    chain: str = "ethereum",
    user: dict = Depends(get_current_user),
):
    return await aave.get_reserve_data(asset, chain)


@router.get("/aave/deposit")
async def aave_simulate_deposit(
    asset: str = Query("USDC"),
    amount: float = Query(1000.0),
    user: dict = Depends(get_current_user),
):
    return await aave.simulate_deposit(asset, amount)


@router.get("/aave/borrow")
async def aave_simulate_borrow(
    asset: str = Query("USDC"),
    amount: float = Query(1000.0),
    user: dict = Depends(get_current_user),
):
    return await aave.simulate_borrow(asset, amount)


@router.get("/curve/pools")
async def curve_pools(user: dict = Depends(get_current_user)):
    return await curve.list_pools()


@router.get("/curve/pool/{pool_id}")
async def curve_pool_detail(pool_id: str, user: dict = Depends(get_current_user)):
    return await curve.get_pool(pool_id)


@router.get("/lido/info")
async def lido_info(user: dict = Depends(get_current_user)):
    return await lido.get_staking_info()


@router.get("/lido/stake")
async def lido_simulate(amount: float = Query(10.0), user: dict = Depends(get_current_user)):
    return await lido.simulate_stake(amount)


@router.get("/yearn/vaults")
async def yearn_vaults(user: dict = Depends(get_current_user)):
    return await yearn.list_vaults()


@router.get("/yearn/vault/{vault_id}")
async def yearn_vault_detail(vault_id: str, user: dict = Depends(get_current_user)):
    return await yearn.get_vault(vault_id)


@router.get("/maker/vault-types")
async def maker_vault_types(user: dict = Depends(get_current_user)):
    return await maker.get_vault_types()


@router.get("/maker/simulate")
async def maker_simulate(
    collateral: str = Query("WETH"),
    deposit: float = Query(10000.0),
    draw: float = Query(5000.0),
    user: dict = Depends(get_current_user),
):
    return await maker.simulate_open_vault(collateral, deposit, draw)
