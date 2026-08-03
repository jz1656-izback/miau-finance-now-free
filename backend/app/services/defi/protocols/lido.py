import logging

logger = logging.getLogger(__name__)


async def get_staking_info() -> dict:
    return {
        "protocol": "Lido",
        "staked_eth": "9,800,000 ETH",
        "total_value": "$32.5B",
        "apy": 3.25,
        "fee_pct": 10.0,
        "staking_assets": [
            {"symbol": "stETH", "name": "Lido Staked ETH", "apy": 3.25, "tvl": "$32.5B"},
            {"symbol": "wstETH", "name": "Lido Wrapped Staked ETH", "apy": 3.25, "tvl": "$28.1B"},
        ],
        "node_operators": 39,
        "validators": 310_000,
    }


async def simulate_stake(amount_eth: float) -> dict:
    steth_rate = 1.0
    steth_amount = round(amount_eth / steth_rate, 4)
    return {
        "amount_eth": amount_eth,
        "estimated_steth": steth_amount,
        "exchange_rate": steth_rate,
        "daily_reward_eth": round(amount_eth * 0.0325 / 365, 6),
        "apy": 3.25,
    }


async def get_withdrawal_status() -> dict:
    return {
        "queued_withdrawals": 1452,
        "estimated_wait_hours": 48,
        "min_withdrawal": "0.01 ETH",
        "max_withdrawal": "1000 ETH",
    }
