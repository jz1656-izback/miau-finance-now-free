import logging

logger = logging.getLogger(__name__)

POOLS = {
    "3pool": {"name": "3Pool", "tokens": ["DAI", "USDC", "USDT"], "tvL": "450M", "fee": 0.01, "apy": 3.2},
    "steth": {"name": "stETH/ETH", "tokens": ["stETH", "ETH"], "tvL": "2.1B", "fee": 0.04, "apy": 2.8},
    "frax": {"name": "FRAX/USDC", "tokens": ["FRAX", "USDC"], "tvL": "800M", "fee": 0.02, "apy": 3.5},
    "tricrypto": {"name": "TriCrypto", "tokens": ["USDT", "WBTC", "WETH"], "tvL": "1.5B", "fee": 0.04, "apy": 4.1},
}


async def list_pools() -> list[dict]:
    return [
        {"id": pid, **pool}
        for pid, pool in POOLS.items()
    ]


async def get_pool(pool_id: str) -> dict:
    pool = POOLS.get(pool_id)
    if not pool:
        return {"error": f"Pool {pool_id} not found"}
    return {"id": pool_id, **pool}


async def simulate_swap(pool_id: str, token_in: str, amount: float) -> dict:
    pool = POOLS.get(pool_id)
    if not pool:
        return {"error": "Pool not found"}
    fee = amount * pool["fee"] / 100
    estimated = amount - fee
    return {
        "pool": pool_id,
        "token_in": token_in,
        "amount_in": amount,
        "fee": round(fee, 4),
        "estimated_out": round(estimated, 4),
        "slippage_pct": 0.02,
    }
