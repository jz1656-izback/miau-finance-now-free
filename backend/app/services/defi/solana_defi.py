"""Solana DeFi integration — Jupiter, Raydium, Marinade."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

JUPITER_API = "https://quote-api.jup.ag/v6"
RAYDIUM_API = "https://api.raydium.io/v2"
MARINADE_API = "https://api.marinade.finance"


async def jupiter_quote(input_mint: str, output_mint: str, amount: int) -> Optional[dict]:
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{JUPITER_API}/quote", params={"inputMint": input_mint, "outputMint": output_mint, "amount": amount, "slippageBps": 50})
            if resp.status_code == 200:
                data = resp.json()
                return {"in_amount": data.get("inAmount"), "out_amount": data.get("outAmount"), "price_impact": data.get("priceImpactPct")}
    except Exception as e:
        logger.warning("Jupiter quote failed: %s", e)
    return None


async def jupiter_swap(quote_response: dict, user_public_key: str) -> Optional[dict]:
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(f"{JUPITER_API}/swap", json={"quoteResponse": quote_response, "userPublicKey": user_public_key, "wrapAndUnwrapSol": True})
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        logger.warning("Jupiter swap failed: %s", e)
    return None


async def raydium_pools() -> list[dict]:
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{RAYDIUM_API}/main/info")
            if resp.status_code == 200:
                data = resp.json()
                return [{"pair": p.get("pair"), "price": p.get("price"), "volume_24h": p.get("volume24h"), "liquidity": p.get("liquidity")} for p in (data.get("pairs", []) or [])[:20]]
    except Exception as e:
        logger.warning("Raydium pools failed: %s", e)
    return []


async def marinade_stake(amount_sol: float) -> Optional[dict]:
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(f"{MARINADE_API}/stake", json={"amount": amount_sol})
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        logger.warning("Marinade stake failed: %s", e)
    return None


async def marinade_stats() -> Optional[dict]:
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{MARINADE_API}/state")
            if resp.status_code == 200:
                data = resp.json()
                return {"msol_price_sol": data.get("msolPrice"), "tvl_sol": data.get("tvlSol"), "apy": data.get("apy")}
    except Exception as e:
        logger.warning("Marinade stats failed: %s", e)
    return None
