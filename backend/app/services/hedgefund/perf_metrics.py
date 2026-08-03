"""Performance metrics — Sharpe, Sortino, Calmar, Omega ratios."""

import logging
from math import sqrt
from typing import Any

logger = logging.getLogger(__name__)


async def sharpe_ratio(returns: list[float], risk_free_rate: float = 0.05) -> float:
    """Annualized Sharpe ratio."""
    n = len(returns)
    if n < 2:
        return 0.0
    avg_ret = sum(returns) / n
    variance = sum((r - avg_ret) ** 2 for r in returns) / (n - 1)
    std = sqrt(variance) if variance > 0 else 0.0001
    excess = avg_ret - risk_free_rate / 252
    annualized = (excess / std) * sqrt(252) if std > 0 else 0
    return round(annualized, 3)


async def sortino_ratio(returns: list[float], risk_free_rate: float = 0.05) -> float:
    """Annualized Sortino ratio (uses downside deviation only)."""
    n = len(returns)
    if n < 2:
        return 0.0
    target = risk_free_rate / 252
    downside = [r - target for r in returns if r < target]
    if not downside:
        return 999.0
    downside_var = sum(d ** 2 for d in downside) / (n - 1)
    downside_std = sqrt(downside_var) if downside_var > 0 else 0.0001
    avg_ret = sum(returns) / n
    annualized = ((avg_ret - target) / downside_std) * sqrt(252) if downside_std > 0 else 0
    return round(annualized, 3)


async def calmar_ratio(returns: list[float], equity_curve: list[float]) -> float:
    """Calmar ratio: annualized return / max drawdown."""
    if len(returns) < 2 or len(equity_curve) < 2:
        return 0.0
    annualized_ret = (sum(returns) / len(returns)) * 252
    from app.services.hedgefund.drawdown_recovery import compute_drawdown
    dd = await compute_drawdown(equity_curve)
    max_dd = dd.get("max_drawdown_pct", 1) / 100
    if max_dd <= 0:
        return 999.0
    return round(annualized_ret / max_dd, 3)


async def omega_ratio(returns: list[float], threshold: float = 0.0) -> float:
    """Omega ratio: probability-weighted ratio of gains vs losses."""
    if not returns:
        return 1.0
    gains = sum(r - threshold for r in returns if r > threshold)
    losses = sum(threshold - r for r in returns if r < threshold)
    if losses <= 0:
        return 999.0
    return round(gains / losses, 3)


async def all_metrics(returns: list[float], equity_curve: list[float]) -> dict:
    """Compute all performance metrics at once."""
    return {
        "sharpe_ratio": await sharpe_ratio(returns),
        "sortino_ratio": await sortino_ratio(returns),
        "calmar_ratio": await calmar_ratio(returns, equity_curve),
        "omega_ratio": await omega_ratio(returns),
        "total_return_pct": round((equity_curve[-1] / equity_curve[0] - 1) * 100, 2) if len(equity_curve) > 1 else 0,
        "annualized_return_pct": round((sum(returns) / len(returns)) * 252 * 100, 2) if returns else 0,
        "volatility_pct": round(sqrt(sum((r - sum(returns)/len(returns))**2 for r in returns) / (len(returns)-1)) * sqrt(252) * 100, 2) if len(returns) > 1 else 0,
    }
