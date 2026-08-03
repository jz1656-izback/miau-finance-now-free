"""CBDC portfolio allocation — multi-CBDC basket optimization, yield optimization."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

CBDC_YIELDS = {"DEUR": 0.035, "ECNY": 0.028, "DUSD": 0.042, "DCJPY": 0.015, "GBP+": 0.038}


async def suggest_allocation(risk_tolerance: str = "moderate") -> dict:
    if risk_tolerance == "conservative":
        weights = {"DEUR": 0.30, "ECNY": 0.10, "DUSD": 0.35, "DCJPY": 0.05, "GBP+": 0.20}
    elif risk_tolerance == "aggressive":
        weights = {"DEUR": 0.15, "ECNY": 0.25, "DUSD": 0.25, "DCJPY": 0.05, "GBP+": 0.30}
    else:
        weights = {"DEUR": 0.25, "ECNY": 0.15, "DUSD": 0.30, "DCJPY": 0.05, "GBP+": 0.25}
    weighted_yield = sum(w * CBDC_YIELDS.get(c, 0) for c, w in weights.items())
    return {"allocation": weights, "weighted_yield": round(weighted_yield * 100, 2), "risk_tolerance": risk_tolerance}


async def rebalance(current: dict, target: dict) -> list[dict]:
    trades = []
    for currency, target_pct in target.items():
        current_pct = current.get(currency, 0)
        diff = target_pct - current_pct
        if abs(diff) > 0.01:
            trades.append({"currency": currency, "action": "buy" if diff > 0 else "sell", "pct": round(abs(diff) * 100, 1)})
    return trades
