"""Multi-CBDC portfolio optimization — optimize across Digital Euro, Yuan, Dollar, Yen, Pound."""

import logging
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional

logger = logging.getLogger(__name__)

_CBDC_ASSETS = [
    {"code": "EUR", "name": "Digital Euro", "central_bank": "ECB", "interest_rate": 0.0375, "volatility": 0.05, "min_investment": 100},
    {"code": "CNY", "name": "Digital Yuan (e-CNY)", "central_bank": "PBOC", "interest_rate": 0.0250, "volatility": 0.08, "min_investment": 100},
    {"code": "USD", "name": "Digital Dollar (FedNow)", "central_bank": "Federal Reserve", "interest_rate": 0.0525, "volatility": 0.04, "min_investment": 100},
    {"code": "JPY", "name": "Digital Yen", "central_bank": "Bank of Japan", "interest_rate": 0.0010, "volatility": 0.07, "min_investment": 100},
    {"code": "GBP", "name": "Digital Pound", "central_bank": "Bank of England", "interest_rate": 0.0475, "volatility": 0.06, "min_investment": 100},
]


_REWARDS = {a["code"]: a["interest_rate"] for a in _CBDC_ASSETS}
_RISKS = {a["code"]: a["volatility"] for a in _CBDC_ASSETS}


def list_cbdc_assets() -> list[dict[str, Any]]:
    return _CBDC_ASSETS


async def optimize_multi_cbdc(
    total_investment: float = 10000.0,
    risk_tolerance: str = "moderate",
    exclude: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Allocate across CBDCs using risk-parity weighting."""
    ex = exclude or []
    assets = [a for a in _CBDC_ASSETS if a["code"] not in ex]

    risk_mult = {"low": 0.5, "moderate": 1.0, "high": 1.5, "extreme": 2.0}
    mult = risk_mult.get(risk_tolerance, 1.0)

    total_risk = sum(_RISKS[a["code"]] for a in assets)
    total_reward = sum(_REWARDS[a["code"]] for a in assets)

    allocations = []
    for a in assets:
        risk_weight = (1 - _RISKS[a["code"]] / total_risk) / (len(assets) - 1) if len(assets) > 1 else 1.0
        reward_weight = _REWARDS[a["code"]] / total_reward if total_reward > 0 else 1.0 / len(assets)
        combined = (risk_weight * 0.6 + reward_weight * 0.4)
        alloc_pct = combined * mult
        alloc_pct = min(max(alloc_pct, 0.05), 0.60)
        alloc_value = total_investment * alloc_pct
        allocations.append({
            "code": a["code"],
            "name": a["name"],
            "interest_rate": a["interest_rate"],
            "volatility": a["volatility"],
            "allocation_pct": round(alloc_pct * 100, 2),
            "allocation_value": round(alloc_value, 2),
            "expected_annual_return": round(alloc_value * a["interest_rate"], 2),
        })

    total_alloc_pct = sum(a["allocation_pct"] for a in allocations)
    if abs(total_alloc_pct - 100) > 5:
        scale = 100.0 / total_alloc_pct
        for a in allocations:
            a["allocation_pct"] = round(a["allocation_pct"] * scale, 2)
            a["allocation_value"] = round(total_investment * a["allocation_pct"] / 100, 2)
            a["expected_annual_return"] = round(a["allocation_value"] * a["interest_rate"], 2)

    total_return = sum(a["expected_annual_return"] for a in allocations)
    return {
        "total_investment": total_investment,
        "risk_tolerance": risk_tolerance,
        "allocations": sorted(allocations, key=lambda x: x["allocation_pct"], reverse=True),
        "summary": {
            "num_assets": len(assets),
            "total_expected_return": round(total_return, 2),
            "expected_yield_pct": round(total_return / total_investment * 100, 2),
            "weighted_risk": round(sum(a["volatility"] * a["allocation_pct"] / 100 for a in allocations) * 100, 2),
        },
    }


async def portfolio_hedge_ratio(
    portfolio_usd: float,
    target_currency: str = "EUR",
) -> dict[str, Any]:
    """Calculate FX hedge ratio for a portfolio into a target CBDC."""
    rates = {
        "EUR": 1.0, "USD": 0.92, "CNY": 0.13, "JPY": 0.0064, "GBP": 1.17,
    }
    rate = rates.get(target_currency, 1.0)
    return {
        "portfolio_value_usd": portfolio_usd,
        "target_currency": target_currency,
        "fx_rate": rate,
        "hedged_value": round(portfolio_usd * rate, 2),
        "hedge_ratio": 1.0,
        "recommendation": f"Full hedge into {target_currency} recommended for USD-based portfolios",
    }
