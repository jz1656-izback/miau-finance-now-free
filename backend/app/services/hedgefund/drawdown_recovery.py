"""Drawdown recovery algorithm."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def compute_drawdown(equity_curve: list[float]) -> dict:
    """Compute drawdown statistics from an equity curve."""
    if len(equity_curve) < 2:
        return {"error": "Insufficient data"}

    peak = equity_curve[0]
    max_dd = 0.0
    max_dd_start = 0
    max_dd_end = 0
    current_dd_start = 0

    for i, val in enumerate(equity_curve):
        if val > peak:
            peak = val
            current_dd_start = i
        dd = (peak - val) / peak if peak > 0 else 0
        if dd > max_dd:
            max_dd = dd
            max_dd_start = current_dd_start
            max_dd_end = i

    final_dd = (peak - equity_curve[-1]) / peak if peak > 0 else 0
    recovery_days = await _estimate_recovery_time(max_dd, equity_curve)

    return {
        "max_drawdown_pct": round(max_dd * 100, 2),
        "max_drawdown_start_idx": max_dd_start,
        "max_drawdown_end_idx": max_dd_end,
        "current_drawdown_pct": round(final_dd * 100, 2),
        "estimated_recovery_days": recovery_days,
        "is_in_drawdown": final_dd > 0.05,
        "severity": _severity(max_dd),
    }


async def recovery_plan(drawdown_pct: float, capital: float, daily_return: float = 0.005) -> dict:
    """Generate a recovery plan given current drawdown."""
    loss_amount = capital * drawdown_pct
    target = capital / (1 - drawdown_pct) if drawdown_pct < 1 else capital * 10
    gain_needed = (target / capital - 1)
    days_to_recover = int(gain_needed / daily_return) if daily_return > 0 else 999

    return {
        "current_capital": round(capital, 2),
        "drawdown_pct": round(drawdown_pct * 100, 2),
        "loss_amount": round(loss_amount, 2),
        "target_capital": round(target, 2),
        "gain_needed_pct": round(gain_needed * 100, 2),
        "estimated_days_to_recover": days_to_recover,
        "suggested_leverage_reduction": min(1.0, drawdown_pct * 3),
        "suggested_risk_reduction": 0.5 if drawdown_pct > 0.15 else 0.8 if drawdown_pct > 0.10 else 1.0,
    }


async def _estimate_recovery_time(max_dd: float, equity_curve: list[float]) -> int:
    """Estimate how many periods to recover from max drawdown."""
    if max_dd <= 0:
        return 0
    gain_needed = max_dd / (1 - max_dd) if max_dd < 1 else 1
    recent = equity_curve[-min(20, len(equity_curve)):]
    if len(recent) < 2:
        return 30
    returns = [(recent[i] - recent[i-1]) / recent[i-1] for i in range(1, len(recent)) if recent[i-1] > 0]
    avg_return = sum(returns) / len(returns) if returns else 0.005
    return int(gain_needed / avg_return) if avg_return > 0 else 999


def _severity(drawdown: float) -> str:
    if drawdown <= 0.05:
        return "mild"
    if drawdown <= 0.10:
        return "moderate"
    if drawdown <= 0.20:
        return "severe"
    if drawdown <= 0.35:
        return "critical"
    return "blow_up"
