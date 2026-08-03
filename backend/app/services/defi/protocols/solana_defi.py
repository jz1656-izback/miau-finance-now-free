import logging

logger = logging.getLogger(__name__)

JUPITER_PAIRS = [
    {"pair": "SOL-USDC", "price": 145.20, "change_24h": 3.2, "volume_24h": "$42M", "liquidity": "$12M"},
    {"pair": "SOL-USDT", "price": 145.15, "change_24h": 3.1, "volume_24h": "$28M", "liquidity": "$8M"},
    {"pair": "BONK-SOL", "price": 0.000024, "change_24h": -5.8, "volume_24h": "$15M", "liquidity": "$3M"},
    {"pair": "JTO-SOL", "price": 3.45, "change_24h": 1.5, "volume_24h": "$8M", "liquidity": "$2.5M"},
    {"pair": "PYTH-SOL", "price": 0.52, "change_24h": 4.2, "volume_24h": "$5M", "liquidity": "$1.8M"},
]

RAYDIUM_POOLS = [
    {"pool": "SOL-USDC", "apy": 18.2, "tvl": "$95M", "volume_24h": "$22M", "fee_pct": 0.25},
    {"pool": "SOL-USDT", "apy": 15.8, "tvl": "$45M", "volume_24h": "$12M", "fee_pct": 0.25},
    {"pool": "RAY-SOL", "apy": 28.5, "tvl": "$18M", "volume_24h": "$6M", "fee_pct": 0.30},
    {"pool": "SRM-SOL", "apy": 22.1, "tvl": "$12M", "volume_24h": "$3M", "fee_pct": 0.30},
]

MARINADE_POOLS = [
    {"validator": "Jito", "stake": "2.1M SOL", "apy": 6.8, "commission_pct": 5.0},
    {"validator": "SolBlaze", "stake": "1.4M SOL", "apy": 6.5, "commission_pct": 4.5},
    {"validator": "JPool", "stake": "0.9M SOL", "apy": 6.3, "commission_pct": 5.5},
]

STAKED_SOL_INFO = {
    "total_staked_sol": "12.5M",
    "mSOL_supply": "11.8M",
    "exchange_rate": 1.06,
    "apy": 6.5,
    "validator_count": 52,
}


async def jupiter_pairs() -> list[dict]:
    return JUPITER_PAIRS


async def jupiter_swap(sol_amount: float, output_mint: str = "USDC") -> dict:
    price = 145.20
    estimated = sol_amount * price
    fee = sol_amount * 0.0001
    return {
        "input": f"{sol_amount} SOL",
        "output": f"{estimated:.2f} {output_mint}",
        "price": price,
        "fee_sol": round(fee, 6),
        "slippage_pct": 0.5,
        "route": ["SOL", "USDC"] if output_mint == "USDC" else ["SOL", output_mint],
    }


async def raydium_pools() -> list[dict]:
    return RAYDIUM_POOLS


async def raydium_simulate_lp(pool: str, sol_amount: float) -> dict:
    return {
        "pool": pool,
        "deposit_sol": sol_amount,
        "estimated_lp_tokens": round(sol_amount * 0.98, 4),
        "estimated_annual_yield": round(sol_amount * 0.18, 4),
        "il_risk_pct": 15.0,
        "fee_tier_pct": 0.25,
    }


async def marinade_info() -> dict:
    return STAKED_SOL_INFO


async def marinade_stake(sol_amount: float) -> dict:
    mSOL = round(sol_amount / 1.06, 4)
    return {
        "stake_sol": sol_amount,
        "receive_mSOL": mSOL,
        "exchange_rate": 1.06,
        "apy": 6.5,
        "unbond_period": "epoch (2-3 days)",
    }
