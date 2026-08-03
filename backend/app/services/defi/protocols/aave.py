import logging

logger = logging.getLogger(__name__)

SUPPORTED_CHAINS = ["ethereum", "arbitrum", "optimism", "polygon", "avalanche"]
SUPPORTED_ASSETS = [
    "WETH", "USDC", "USDT", "DAI", "WBTC", "LINK", "AAVE",
    "MATIC", "AVAX", "OP", "ARB",
]


async def get_reserve_data(asset: str, chain: str = "ethereum") -> dict:
    rates = _mock_rates(asset)
    return {
        "asset": asset.upper(),
        "chain": chain,
        "liquidity_rate_pct": rates["deposit_apy"],
        "variable_borrow_rate_pct": rates["variable_apy"],
        "stable_borrow_rate_pct": rates["stable_apy"],
        "liquidity": rates["liquidity"],
        "available": rates["available"],
        "ltv_pct": rates["ltv"],
        "liquidation_threshold_pct": rates["liq_threshold"],
        "liquidation_penalty_pct": rates["liq_penalty"],
    }


async def simulate_deposit(asset: str, amount: float) -> dict:
    rates = _mock_rates(asset)
    return {
        "asset": asset.upper(),
        "amount": amount,
        "estimated_apy": rates["deposit_apy"],
        "daily_yield": round(amount * rates["deposit_apy"] / 365 / 100, 4),
        "monthly_yield": round(amount * rates["deposit_apy"] / 12 / 100, 4),
    }


async def simulate_borrow(asset: str, amount: float) -> dict:
    rates = _mock_rates(asset)
    return {
        "asset": asset.upper(),
        "amount": amount,
        "variable_rate_apy": rates["variable_apy"],
        "stable_rate_apy": rates["stable_apy"],
        "daily_interest": round(amount * rates["variable_apy"] / 365 / 100, 4),
        "health_factor": 2.5,
    }


def _mock_rates(asset: str) -> dict:
    base = {
        "WETH": {"deposit_apy": 2.5, "variable_apy": 3.8, "stable_apy": 4.2, "ltv": 82.5, "liq_threshold": 86.0, "liq_penalty": 5.0, "liquidity": "500M", "available": "120M"},
        "USDC": {"deposit_apy": 4.8, "variable_apy": 6.5, "stable_apy": 7.0, "ltv": 82.5, "liq_threshold": 86.0, "liq_penalty": 5.0, "liquidity": "2.1B", "available": "850M"},
        "USDT": {"deposit_apy": 4.6, "variable_apy": 6.2, "stable_apy": 6.8, "ltv": 80.0, "liq_threshold": 84.0, "liq_penalty": 5.0, "liquidity": "1.8B", "available": "720M"},
        "DAI":  {"deposit_apy": 4.5, "variable_apy": 6.0, "stable_apy": 6.5, "ltv": 80.0, "liq_threshold": 84.0, "liq_penalty": 5.0, "liquidity": "900M", "available": "340M"},
        "WBTC": {"deposit_apy": 1.2, "variable_apy": 2.5, "stable_apy": 3.0, "ltv": 75.0, "liq_threshold": 80.0, "liq_penalty": 7.5, "liquidity": "400M", "available": "80M"},
    }
    return base.get(asset.upper(), {"deposit_apy": 3.0, "variable_apy": 5.0, "stable_apy": 5.5, "ltv": 75.0, "liq_threshold": 80.0, "liq_penalty": 5.0, "liquidity": "100M", "available": "30M"})
