import logging

logger = logging.getLogger(__name__)

COLLATERAL_TYPES = [
    {"ilk": "ETH-A", "collateral": "WETH", "ratio": 145, "liquidation_ratio": 170, "stability_fee_pct": 0.5, "debt_ceiling": "10B"},
    {"ilk": "ETH-B", "collateral": "WETH", "ratio": 130, "liquidation_ratio": 150, "stability_fee_pct": 0.75, "debt_ceiling": "2B"},
    {"ilk": "ETH-C", "collateral": "WETH", "ratio": 170, "liquidation_ratio": 200, "stability_fee_pct": 0.35, "debt_ceiling": "5B"},
    {"ilk": "WBTC-A", "collateral": "WBTC", "ratio": 145, "liquidation_ratio": 170, "stability_fee_pct": 0.5, "debt_ceiling": "2B"},
    {"ilk": "USDC-A", "collateral": "USDC", "ratio": 101, "liquidation_ratio": 110, "stability_fee_pct": 0.0, "debt_ceiling": "10B"},
    {"ilk": "RETH-A", "collateral": "rETH", "ratio": 145, "liquidation_ratio": 170, "stability_fee_pct": 0.5, "debt_ceiling": "500M"},
    {"ilk": "STETH-A", "collateral": "stETH", "ratio": 160, "liquidation_ratio": 185, "stability_fee_pct": 0.5, "debt_ceiling": "2.5B"},
]


async def get_vault_types() -> list[dict]:
    return COLLATERAL_TYPES


async def simulate_open_vault(collateral: str, deposit_amount: float, draw_amount: float) -> dict:
    ratio = round(draw_amount / deposit_amount * 100, 1) if deposit_amount > 0 else 0
    liq_price = round(deposit_amount * 0.7, 2)
    return {
        "collateral": collateral,
        "deposit_usd": deposit_amount,
        "draw_dai": draw_amount,
        "collateralization_ratio_pct": ratio,
        "liquidation_price_usd": liq_price,
        "stability_fee_annual_pct": 0.5,
        "annual_fee_dai": round(draw_amount * 0.005, 2),
        "max_drawable": round(deposit_amount * 0.65, 2),
    }


async def get_dai_info() -> dict:
    return {
        "peg": 1.001,
        "total_supply": "5.2B DAI",
        "total_collateral": "$7.8B",
        "collateralization_ratio_pct": 145.0,
        "dai_savings_rate_pct": 3.75,
        "protocol_revenue_annual": "$120M",
    }
