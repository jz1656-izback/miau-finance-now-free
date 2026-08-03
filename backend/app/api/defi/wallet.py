"""Wallet API endpoints."""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.defi.walletconnect import create_session, list_sessions, get_session, disconnect, switch_chain, generate_uri, SUPPORTED_CHAINS
from app.services.defi.balance_aggregator import aggregate_all

router = APIRouter(prefix="/wallet", tags=["DeFi Wallet"])


@router.get("/chains")
async def supported_chains():
    return {"chains": [{"id": k, **v} for k, v in SUPPORTED_CHAINS.items()]}


@router.post("/connect")
async def wallet_connect(
    address: str,
    chain: str = "ethereum",
    user: dict = Depends(get_current_user),
):
    if chain not in SUPPORTED_CHAINS:
        raise HTTPException(400, f"Unsupported chain: {chain}")
    uri = generate_uri()
    session = await create_session(address, chain, {"user": user.get("sub")})
    return {"uri": uri, "session": session}


@router.get("/sessions")
async def wallet_sessions():
    return {"sessions": await list_sessions(), "total": len(await list_sessions())}


@router.get("/sessions/{topic}")
async def wallet_session(topic: str):
    s = await get_session(topic)
    if not s:
        raise HTTPException(404, "Session not found")
    return s


@router.post("/sessions/{topic}/disconnect")
async def wallet_disconnect(topic: str):
    if not await disconnect(topic):
        raise HTTPException(404, "Session not found")
    return {"status": "disconnected"}


@router.post("/sessions/{topic}/chain")
async def wallet_switch_chain(topic: str, chain: str):
    s = await switch_chain(topic, chain)
    if not s:
        raise HTTPException(404, "Session not found")
    return s


@router.post("/balances")
async def wallet_balances(
    addresses: dict[str, list[str]],
    user: dict = Depends(get_current_user),
):
    return await aggregate_all(addresses)
