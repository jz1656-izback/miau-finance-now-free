"""Dynamic position sizing — Kelly criterion and fractional Kelly."""

import logging
from math import erf, sqrt
from typing import Any

logger = logging.getLogger(__name__)


async def kelly_fraction(win_prob: float, avg_win: float, avg_loss: float) -> float:
    """Compute full Kelly fraction: f* = p - q/b where b = win/loss ratio."""
    if avg_loss <= 0:
        return 0
    b = avg_win / avg_loss
    q = 1 - win_prob
    f = win_prob - q / b if b > 0 else 0
    return max(0.0, min(f, 1.0))


async def fractional_kelly(win_prob: float, avg_win: float, avg_loss: float, fraction: float = 0.25) -> float:
    """Fractional Kelly — use a portion of full Kelly to reduce volatility."""
    full = await kelly_fraction(win_prob, avg_win, avg_loss)
    return full * fraction


async def position_size(
    capital: float,
    price: float,
    win_prob: float,
    avg_win: float,
    avg_loss: float,
    risk_multiplier: float = 1.0,
    max_single_position_pct: float = 0.25,
) -> dict:
    """Compute recommended position size using fractional Kelly."""
    f = await kelly_fraction(win_prob, avg_win, avg_loss)
    f_frac = f * risk_multiplier * 0.25
    f_frac = min(f_frac, max_single_position_pct)

    shares = int(capital * f_frac / price) if price > 0 else 0
    position_value = shares * price
    pct_of_capital = position_value / capital if capital > 0 else 0

    return {
        "kelly_fraction": round(f, 4),
        "recommended_pct": round(f_frac * 100, 2),
        "recommended_shares": shares,
        "position_value": round(position_value, 2),
        "pct_of_capital": round(pct_of_capital * 100, 2),
        "max_allowed_pct": max_single_position_pct * 100,
        "risk_multiplier": risk_multiplier,
    }


async def max_drawdown_position(current_drawdown: float, max_drawdown_limit: float = 0.25) -> float:
    """Reduce position size when drawdown exceeds limits."""
    if current_drawdown <= 0:
        return 1.0
    if current_drawdown >= max_drawdown_limit:
        return 0.0
    return 1.0 - (current_drawdown / max_drawdown_limit)
