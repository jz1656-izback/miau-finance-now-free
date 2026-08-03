from decimal import Decimal
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FillResult:
    filled_qty: Decimal
    fill_price: Decimal
    commission: Decimal
    slippage: Decimal
    timestamp: datetime


class FillSimulator:
    def __init__(self, slippage_pct: Decimal = Decimal("0.0005"), commission_pct: Decimal = Decimal("0.001")):
        self.slippage_pct = slippage_pct
        self.commission_pct = commission_pct

    def simulate_fill(self, order_side: str, quantity: Decimal, price: Decimal, current_price: Optional[Decimal] = None) -> FillResult:
        exec_price = Decimal(str(current_price or price))
        qty = Decimal(str(quantity))
        if order_side == "BUY":
            fill_price = exec_price * (Decimal("1") + self.slippage_pct)
            slippage = (fill_price - exec_price) * qty
        else:
            fill_price = exec_price * (Decimal("1") - self.slippage_pct)
            slippage = (exec_price - fill_price) * qty
        notional = fill_price * qty
        commission = notional * self.commission_pct
        return FillResult(
            filled_qty=qty,
            fill_price=fill_price,
            commission=commission,
            slippage=slippage,
            timestamp=datetime.now(),
        )
        return FillResult(
            filled_qty=quantity,
            fill_price=fill_price,
            commission=commission,
            slippage=slippage,
            timestamp=datetime.now(),
        )
