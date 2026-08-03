from decimal import Decimal
from typing import Optional


def calculate_slippage(
    notional: Decimal,
    volume: Optional[int] = None,
    volatility: Optional[Decimal] = None,
    model: str = "fixed",
) -> Decimal:
    n = Decimal(str(notional))
    if model == "fixed":
        return n * Decimal("0.0005")
    elif model == "volume_based" and volume and volume > 0:
        participation = float(n) / float(volume)
        return n * Decimal(str(min(participation * 0.01, 0.01)))
    elif model == "volatility_based" and volatility:
        return n * Decimal(str(volatility))
    return Decimal("0")
