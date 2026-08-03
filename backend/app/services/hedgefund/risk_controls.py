"""Stop-loss and take-profit automation."""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


async def trailing_stop(current_price: float, entry_price: float, trail_pct: float = 0.05) -> dict:
    """Trailing stop-loss: triggers when price drops trail_pct from its peak."""
    peak = max(entry_price, current_price)
    stop_price = peak * (1 - trail_pct)
    triggered = current_price <= stop_price
    return {
        "entry_price": entry_price,
        "peak_price": peak,
        "stop_price": round(stop_price, 2),
        "current_price": current_price,
        "trail_pct": trail_pct,
        "triggered": triggered,
        "action": "SELL" if triggered else "HOLD",
    }


async def take_profit(current_price: float, entry_price: float, profit_target_pct: float = 0.15) -> dict:
    """Take-profit: triggers when price rises profit_target_pct above entry."""
    target_price = entry_price * (1 + profit_target_pct)
    triggered = current_price >= target_price
    profit_pct = (current_price / entry_price - 1) if entry_price > 0 else 0
    return {
        "entry_price": entry_price,
        "target_price": round(target_price, 2),
        "current_price": current_price,
        "profit_target_pct": profit_target_pct,
        "achieved_pct": round(profit_pct * 100, 2),
        "triggered": triggered,
        "action": "SELL" if triggered else "HOLD",
    }


async def combined_risk_check(
    current_price: float,
    entry_price: float,
    trail_pct: float = 0.05,
    profit_target_pct: float = 0.15,
    max_loss_pct: float = 0.10,
) -> dict:
    """Combined stop-loss, take-profit, and hard stop."""
    trailing = await trailing_stop(current_price, entry_price, trail_pct)
    tp = await take_profit(current_price, entry_price, profit_target_pct)
    hard_stop_price = entry_price * (1 - max_loss_pct)
    hard_stop_triggered = current_price <= hard_stop_price

    action = "HOLD"
    if tp["triggered"]:
        action = "SELL_TAKE_PROFIT"
    elif trailing["triggered"]:
        action = "SELL_TRAILING_STOP"
    elif hard_stop_triggered:
        action = "SELL_HARD_STOP"

    return {
        "action": action,
        "current_price": current_price,
        "entry_price": entry_price,
        "trailing_stop": trailing,
        "take_profit": tp,
        "hard_stop": {
            "price": round(hard_stop_price, 2),
            "triggered": hard_stop_triggered,
            "max_loss_pct": max_loss_pct,
        },
    }
