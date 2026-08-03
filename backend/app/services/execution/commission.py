from decimal import Decimal


def calculate_commission(notional: Decimal, schedule: str = "default") -> Decimal:
    if schedule == "per_share":
        return Decimal(str(max(1, int(notional / Decimal("100"))))) * Decimal("0.005")
    elif schedule == "fixed":
        return Decimal("1.00")
    elif schedule == "tiered":
        if notional < Decimal("10000"):
            return Decimal("1.50")
        elif notional < Decimal("100000"):
            return Decimal("3.00")
        else:
            return Decimal("5.00")
    return notional * Decimal("0.001")
