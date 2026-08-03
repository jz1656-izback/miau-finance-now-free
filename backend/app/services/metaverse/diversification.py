"""Metaverse diversification analysis.

Computes correlation between virtual world assets and traditional
financial instruments, producing a diversification score and
allocation recommendations.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Stub correlation matrix: virtual worlds vs each other and vs traditional assets
# In production these would come from a real data source
_VIRTUAL_CORRELATIONS: dict[str, dict[str, float]] = {
    "decentraland": {"sandbox": 0.72, "somnium": 0.58, "voxels": 0.61, "cryptovoxels": 0.55},
    "sandbox": {"decentraland": 0.72, "somnium": 0.63, "voxels": 0.59, "cryptovoxels": 0.52},
    "somnium": {"decentraland": 0.58, "sandbox": 0.63, "voxels": 0.67, "cryptovoxels": 0.60},
    "voxels": {"decentraland": 0.61, "sandbox": 0.59, "somnium": 0.67, "cryptovoxels": 0.64},
    "cryptovoxels": {"decentraland": 0.55, "sandbox": 0.52, "somnium": 0.60, "voxels": 0.64},
}

TRADITIONAL_CORRELATIONS: dict[str, float] = {
    "sp500": 0.12, "nasdaq": 0.18, "gold": -0.05, "real_estate": 0.25, "crypto": 0.45,
}

ALL_WORLDS = sorted(_VIRTUAL_CORRELATIONS.keys())


def correlation_matrix(worlds: list[str] | None = None) -> dict[str, dict[str, float]]:
    worlds = worlds or ALL_WORLDS
    matrix: dict[str, dict[str, float]] = {}
    for w in worlds:
        matrix[w] = {}
        for w2 in worlds:
            if w == w2:
                matrix[w][w2] = 1.0
            else:
                matrix[w][w2] = _VIRTUAL_CORRELATIONS.get(w, {}).get(w2, 0.5)
    return matrix


def compute_diversification_score(allocations: dict[str, float]) -> dict[str, Any]:
    if not allocations:
        return {"score": 0, "verdict": "No allocations provided"}

    worlds = [k for k in allocations if k in _VIRTUAL_CORRELATIONS]
    weights = [allocations[w] for w in worlds]
    total = sum(weights)
    if total == 0:
        return {"score": 0, "verdict": "Zero allocation weight"}

    weights = [w / total for w in weights]
    corr = correlation_matrix(worlds)
    weighted_corr = 0.0
    pair_count = 0
    for i, w1 in enumerate(worlds):
        for j, w2 in enumerate(worlds):
            if i < j:
                weighted_corr += weights[i] * weights[j] * corr[w1][w2]
                pair_count += 1

    avg_corr = weighted_corr / pair_count if pair_count else 0
    score = round((1 - avg_corr) * 100, 1)

    if score >= 70:
        verdict = "Well diversified across virtual worlds"
    elif score >= 40:
        verdict = "Moderate diversification — consider adding uncorrelated worlds"
    else:
        verdict = "Highly concentrated — spread allocations across more worlds"

    return {
        "score": score,
        "verdict": verdict,
        "average_correlation": round(avg_corr, 3),
        "worlds": worlds,
        "traditional_correlations": TRADITIONAL_CORRELATIONS,
    }


def suggest_optimal_allocation(
    risk_tolerance: str = "moderate",
    target_worlds: list[str] | None = None,
) -> dict[str, Any]:
    targets = target_worlds or ALL_WORLDS
    n = len(targets)
    if n == 0:
        return {"allocation": {}, "note": "No worlds specified"}

    base = round(1.0 / n, 3)
    alloc = {w: base for w in targets}

    if risk_tolerance == "conservative":
        alloc[targets[0]] = round(base * 1.5, 3)
    elif risk_tolerance == "aggressive":
        alloc[targets[-1]] = round(base * 1.5, 3)

    remaining = 1.0 - sum(alloc.values())
    if remaining != 0:
        alloc[targets[0]] = round(alloc[targets[0]] + remaining, 3)

    score_result = compute_diversification_score(alloc)
    return {
        "allocation": alloc,
        "risk_tolerance": risk_tolerance,
        "diversification_score": score_result["score"],
        "verdict": score_result["verdict"],
    }
