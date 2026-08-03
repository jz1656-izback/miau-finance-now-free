import logging

logger = logging.getLogger(__name__)

VAULTS = {
    "yvUSDC": {"name": "yearn USDC Vault", "token": "USDC", "apy": 5.8, "tvl": "$420M", "strategy": "Lend + LP"},
    "yvWETH": {"name": "yearn WETH Vault", "token": "WETH", "apy": 3.2, "tvl": "$310M", "strategy": "Liquid Staking + Lend"},
    "yvDAI": {"name": "yearn DAI Vault", "token": "DAI", "apy": 5.5, "tvl": "$180M", "strategy": "Lend + Curve LP"},
    "yvWBTC": {"name": "yearn WBTC Vault", "token": "WBTC", "apy": 2.1, "tvl": "$95M", "strategy": "Lend"},
    "yvYFI": {"name": "yearn YFI Vault", "token": "YFI", "apy": 4.5, "tvl": "$22M", "strategy": "Stake + Lend"},
}


async def list_vaults() -> list[dict]:
    return [{"id": vid, **v} for vid, v in VAULTS.items()]


async def get_vault(vault_id: str) -> dict:
    v = VAULTS.get(vault_id)
    if not v:
        return {"error": f"Vault {vault_id} not found"}
    return {"id": vault_id, **v}


async def simulate_deposit(vault_id: str, amount: float) -> dict:
    v = VAULTS.get(vault_id)
    if not v:
        return {"error": "Vault not found"}
    daily = round(amount * v["apy"] / 365 / 100, 4)
    monthly = round(amount * v["apy"] / 12 / 100, 4)
    yearly = round(amount * v["apy"] / 100, 4)
    return {
        "vault": vault_id,
        "token": v["token"],
        "amount": amount,
        "estimated_apy": v["apy"],
        "daily_yield": daily,
        "monthly_yield": monthly,
        "yearly_yield": yearly,
        "strategy": v["strategy"],
    }
