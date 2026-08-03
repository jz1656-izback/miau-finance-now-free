"""Portfolio risk budgeting — risk parity allocation across strategies."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def risk_parity_weights(risks: dict[str, float], target_vol: float = 0.15) -> dict[str, float]:
    """Compute risk parity weights so each asset contributes equally to portfolio risk."""
    total_inverse = sum(1 / max(r, 0.001) for r in risks.values())
    weights = {k: (1 / max(v, 0.001)) / total_inverse for k, v in risks.items()}
    scaled = {k: w * target_vol for k, w in weights.items()}
    total = sum(scaled.values())
    return {k: v / total for k, v in scaled.items()} if total > 0 else weights


async def compute_portfolio_risk(weights: dict[str, float], cov_matrix: dict[str, dict[str, float]]) -> float:
    """Compute portfolio variance given weights and covariance."""
    variance = 0.0
    for a, wa in weights.items():
        for b, wb in weights.items():
            cov = cov_matrix.get(a, {}).get(b, 0) or cov_matrix.get(b, {}).get(a, 0)
            variance += wa * wb * cov
    return variance ** 0.5 if variance > 0 else 0.0


async def budget_report(weights: dict[str, float], total_capital: float) -> list[dict]:
    """Generate a per-strategy budget breakdown."""
    return [
        {"strategy": k, "weight_pct": round(w * 100, 2), "allocated": round(w * total_capital, 2)}
        for k, w in sorted(weights.items(), key=lambda x: -x[1])
    ]
