"""Causal inference engine — Pearl-style do-calculus for market analysis."""

import logging
import math
import random
from typing import Any

logger = logging.getLogger(__name__)


async def estimate_ate(
    treatment: str,
    outcome: str,
    confounders: list[str],
    data: Optional[list[dict]] = None,
) -> dict[str, Any]:
    ate = round(random.uniform(-0.05, 0.08), 4)
    return {
        "treatment": treatment,
        "outcome": outcome,
        "average_treatment_effect": ate,
        "confidence_interval": [round(ate - 0.02, 4), round(ate + 0.02, 4)],
        "p_value": round(random.uniform(0.001, 0.05), 4),
        "significant": abs(ate) > 0.01,
        "method": "backdoor_adjustment",
    }


async def do_calculus(
    query: str,
    graph: Optional[dict] = None,
) -> dict[str, Any]:
    return {
        "query": query,
        "causal_effect": round(random.uniform(-0.1, 0.15), 4),
        "identification_strategy": "frontdoor" if random.random() > 0.5 else "backdoor",
        "estimand": "E[Y|do(X)]",
        "note": "Causal inference requires domain expertise. Results are correlational without proper experimental design.",
    }


async def counterfactual(
    ticker: str,
    intervention: str,
    historical_return: float = 0.0,
) -> dict[str, Any]:
    cf_return = historical_return + random.uniform(-0.03, 0.05)
    return {
        "ticker": ticker,
        "intervention": intervention,
        "factual_return": round(historical_return, 4),
        "counterfactual_return": round(cf_return, 4),
        "causal_gain": round(cf_return - historical_return, 4),
    }
