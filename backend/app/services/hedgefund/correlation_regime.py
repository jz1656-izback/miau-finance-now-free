"""Correlation regime detection — identify market correlation regimes."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def detect_regime(correlations: list[float], window: int = 20) -> dict:
    """Classify the current correlation regime based on recent correlation history."""
    if len(correlations) < window:
        return {"regime": "insufficient_data", "avg_correlation": 0, "regime_score": 0}

    recent = correlations[-window:]
    avg_corr = sum(recent) / len(recent)
    max_corr = max(recent)
    min_corr = min(recent)
    trend = "increasing" if len(recent) > 5 and recent[-1] > recent[-5] else "decreasing" if len(recent) > 5 and recent[-1] < recent[-5] else "stable"

    if avg_corr > 0.7:
        regime = "high_correlation"
        desc = "Assets move together — crisis regime or broad market moves"
    elif avg_corr > 0.4:
        regime = "moderate_correlation"
        desc = "Typical market conditions with sector rotation"
    elif avg_corr > 0.1:
        regime = "low_correlation"
        desc = "Favorable for diversification and stock-picking"
    else:
        regime = "negative_correlation"
        desc = "Divergent markets — potential regime change or flight to safety"

    regime_score = avg_corr
    if trend == "increasing":
        regime_score *= 1.1

    return {
        "regime": regime,
        "description": desc,
        "avg_correlation": round(avg_corr, 3),
        "max_correlation": round(max_corr, 3),
        "min_correlation": round(min_corr, 3),
        "trend": trend,
        "regime_score": round(min(regime_score, 1.0), 3),
        "window": window,
    }


async def regime_to_risk_multiplier(regime: str) -> float:
    """Map correlation regime to a risk multiplier for position sizing."""
    multipliers = {
        "high_correlation": 0.5,
        "moderate_correlation": 0.8,
        "low_correlation": 1.0,
        "negative_correlation": 1.2,
    }
    return multipliers.get(regime, 1.0)
