import logging
from typing import Optional

logger = logging.getLogger(__name__)

SUPPORTED_CHAINS = {
    "ethereum": 1, "arbitrum": 42161, "optimism": 10,
    "polygon": 137, "base": 8453, "avalanche": 43114,
}


async def get_pool_info(pool_address: str, chain: str = "ethereum") -> dict:
    try:
        from web3 import Web3
        from web3.middleware import geth_poa_middleware
        rpc_urls = {
            "ethereum": "https://eth.llamarpc.com",
            "arbitrum": "https://arbitrum.llamarpc.com",
            "optimism": "https://optimism.llamarpc.com",
            "polygon": "https://polygon.llamarpc.com",
        }
        w3 = Web3(Web3.HTTPProvider(rpc_urls.get(chain, rpc_urls["ethereum"])))
        checksum = Web3.to_checksum_address(pool_address)
        pool_abi = [
            {"inputs": [], "name": "slot0", "outputs": [{"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "liquidity", "outputs": [{"internalType": "uint128", "name": "", "type": "uint128"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "fee", "outputs": [{"internalType": "uint24", "name": "", "type": "uint24"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "token0", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
            {"inputs": [], "name": "token1", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
        ]
        pool = w3.eth.contract(address=checksum, abi=pool_abi)
        slot0 = pool.functions.slot0().call()
        liquidity = pool.functions.liquidity().call()
        fee = pool.functions.fee().call()
        token0 = pool.functions.token0().call()
        token1 = pool.functions.token1().call()
        sqrt_price = slot0[0] / 2**96
        price = sqrt_price ** 2
        return {
            "pool": pool_address,
            "chain": chain,
            "token0": token0,
            "token1": token1,
            "price": round(price, 6),
            "liquidity": str(liquidity),
            "fee_pct": fee / 10000,
            "sqrt_price_x96": slot0[0],
        }
    except ImportError:
        return {"error": "web3 library not installed — run: pip install web3"}
    except Exception as e:
        logger.warning("Failed to fetch Uniswap pool %s: %s", pool_address, e)
        return {"error": str(e)}


async def simulate_swap(
    token_in: str,
    token_out: str,
    amount_in: float,
    chain: str = "ethereum",
) -> dict:
    return {
        "token_in": token_in,
        "token_out": token_out,
        "amount_in": amount_in,
        "estimated_out": round(amount_in * 0.997, 4),
        "price_impact_pct": 0.05,
        "route": [token_in, token_out],
        "chain": chain,
    }
