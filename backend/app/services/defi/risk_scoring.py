"""DeFi risk scoring — protocol risk, impermanent loss, smart contract risk."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

PROTOCOL_RISK: dict[str, dict] = {
    "uniswap": {"name": "Uniswap", "audit_score": 95, "tvl_b": 5.2, "age_years": 5, "hacks": 0, "risk_level": "low"},
    "aave": {"name": "Aave", "audit_score": 92, "tvl_b": 12.0, "age_years": 4, "hacks": 0, "risk_level": "low"},
    "curve": {"name": "Curve", "audit_score": 88, "tvl_b": 3.5, "age_years": 4, "hacks": 1, "risk_level": "medium"},
    "lido": {"name": "Lido", "audit_score": 90, "tvl_b": 25.0, "age_years": 3, "hacks": 0, "risk_level": "low"},
    "maker": {"name": "MakerDAO", "audit_score": 93, "tvl_b": 7.0, "age_years": 6, "hacks": 0, "risk_level": "low"},
    "yearn": {"name": "Yearn Finance", "audit_score": 85, "tvl_b": 2.0, "age_years": 4, "hacks": 1, "risk_level": "medium"},
    "jupiter": {"name": "Jupiter", "audit_score": 80, "tvl_b": 1.5, "age_years": 2, "hacks": 0, "risk_level": "medium"},
    "raydium": {"name": "Raydium", "audit_score": 75, "tvl_b": 0.8, "age_years": 3, "hacks": 1, "risk_level": "high"},
}


def score_protocol(protocol_id: str) -> Optional[dict]:
    p = PROTOCOL_RISK.get(protocol_id.lower())
    if not p:
        return None
    audit = p["audit_score"] / 100
    tvl_factor = min(p["tvl_b"] / 10, 1.0)
    age_factor = min(p["age_years"] / 5, 1.0)
    hack_penalty = max(0, 1.0 - p["hacks"] * 0.15)
    composite = (audit * 0.4 + tvl_factor * 0.2 + age_factor * 0.2 + hack_penalty * 0.2) * 100
    return {"protocol": p["name"], "composite_score": round(composite, 1), "risk_level": p["risk_level"], "audit_score": p["audit_score"], "tvl_b": p["tvl_b"]}


def score_portfolio(positions: list[dict]) -> dict:
    scores = [score_protocol(p.get("protocol", "")) for p in positions]
    scores = [s for s in scores if s]
    if not scores:
        return {"weighted_score": 0, "risk_level": "unknown", "positions": 0}
    weighted = sum(s["composite_score"] for s in scores) / len(scores)
    levels = {"low": 0, "medium": 1, "high": 2}
    avg_level = sum(levels.get(s["risk_level"], 1) for s in scores) / len(scores)
    risk = "low" if avg_level < 0.5 else "medium" if avg_level < 1.5 else "high"
    return {"weighted_score": round(weighted, 1), "risk_level": risk, "positions": len(scores), "protocols": scores}
