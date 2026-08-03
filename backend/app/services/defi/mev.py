"""MEV protection suggestions and sandwich attack detection."""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


async def estimate_mev_risk(tx_params: dict[str, Any]) -> dict[str, Any]:
    risk_score = 0
    flags = []

    value = float(tx_params.get("value", 0))
    if value > 10:
        risk_score += 30
        flags.append("high_value")

    slippage = tx_params.get("slippage", 0.5)
    if slippage > 1.0:
        risk_score += 20
        flags.append("high_slippage")

    if tx_params.get("frontrun", False):
        risk_score += 40
        flags.append("frontrun_risk")

    return {
        "risk_score": min(risk_score, 100),
        "risk_level": "high" if risk_score > 60 else "medium" if risk_score > 30 else "low",
        "flags": flags,
        "suggestions": _suggestions(flags),
    }


def _suggestions(flags: list[str]) -> list[str]:
    suggestions = []
    if "high_value" in flags:
        suggestions.append("Split into smaller transactions")
    if "high_slippage" in flags:
        suggestions.append("Set slippage to 0.5% or lower")
    if "frontrun_risk" in flags:
        suggestions.append("Use a private mempool (Flashbots, bloxroute)")
    if not suggestions:
        suggestions.append("Transaction appears safe")
    return suggestions
