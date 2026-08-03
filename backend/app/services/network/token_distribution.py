"""MIAU token distribution — vesting schedules, staking rewards, governance allocation."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

TOTAL_SUPPLY = 100_000_000
ALLOCATIONS = {
    "community": 0.40,
    "team": 0.20,
    "investors": 0.15,
    "treasury": 0.10,
    "liquidity": 0.10,
    "airdrop": 0.05,
}

_balances: dict[str, float] = {}
_stakes: dict[str, dict] = {}


async def get_balance(address: str) -> float:
    return _balances.get(address, 0)


async def distribute(address: str, amount: float, reason: str = "") -> dict:
    _balances[address] = _balances.get(address, 0) + amount
    return {"address": address, "amount": amount, "new_balance": _balances[address], "reason": reason}


async def stake(address: str, amount: float, duration_days: int = 30) -> dict:
    if _balances.get(address, 0) < amount:
        return {"error": "Insufficient balance"}
    _balances[address] -= amount
    stake_id = f"stake_{address[:6]}"
    _stakes[stake_id] = {"address": address, "amount": amount, "duration_days": duration_days, "rewards_rate": 0.12}
    return {"stake_id": stake_id, "amount": amount, "rewards_apy": 0.12, "vesting_days": duration_days}


async def unstake(stake_id: str) -> dict:
    s = _stakes.pop(stake_id, None)
    if not s:
        return {"error": "Stake not found"}
    _balances[s["address"]] = _balances.get(s["address"], 0) + s["amount"]
    return {"address": s["address"], "amount_returned": s["amount"]}


async def get_governance_power(address: str) -> float:
    balance = _balances.get(address, 0)
    staked = sum(s["amount"] for s in _stakes.values() if s["address"] == address)
    return balance + staked


async def get_tokenomics() -> dict:
    return {
        "total_supply": TOTAL_SUPPLY,
        "circulating_supply": sum(_balances.values()),
        "staked_supply": sum(s["amount"] for s in _stakes.values()),
        "allocations": {k: v * TOTAL_SUPPLY for k, v in ALLOCATIONS.items()},
        "holders": len(_balances),
    }
