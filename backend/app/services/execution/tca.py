from decimal import Decimal
from dataclasses import dataclass


@dataclass
class TCAResult:
    commission: Decimal
    slippage: Decimal
    market_impact: Decimal
    spread_cost: Decimal
    total_cost: Decimal


def calculate_tca(
    notional: Decimal,
    commission: Decimal,
    slippage: Decimal,
    bid_ask_spread: Decimal = Decimal("0.0001"),
    market_impact_pct: Decimal = Decimal("0.0002"),
) -> TCAResult:
    spread_cost = notional * bid_ask_spread
    market_impact = notional * market_impact_pct
    total = commission + slippage + spread_cost + market_impact
    return TCAResult(
        commission=commission,
        slippage=slippage,
        market_impact=market_impact,
        spread_cost=spread_cost,
        total_cost=total,
    )
