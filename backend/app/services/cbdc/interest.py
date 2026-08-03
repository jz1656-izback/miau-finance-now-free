import logging
from datetime import datetime

logger = logging.getLogger(__name__)

CBDC_RATES = {
    "DEUR": {"rate_pct": 3.25, "next_decision": "2026-06-15", "trend": "stable", "central_bank": "ECB"},
    "ECNY": {"rate_pct": 1.75, "next_decision": "2026-06-20", "trend": "stable", "central_bank": "PBOC"},
    "DUSD": {"rate_pct": 4.50, "next_decision": "2026-06-12", "trend": "stable", "central_bank": "Federal Reserve"},
    "DCJPY": {"rate_pct": 0.10, "next_decision": "2026-06-16", "trend": "stable", "central_bank": "BOJ"},
    "GBP+": {"rate_pct": 4.25, "next_decision": "2026-06-20", "trend": "stable", "central_bank": "BOE"},
}

RATE_HISTORY = {
    "DEUR": [{"date": "2026-01", "rate": 3.50}, {"date": "2026-03", "rate": 3.25}, {"date": "2026-05", "rate": 3.25}],
    "ECNY": [{"date": "2026-01", "rate": 1.50}, {"date": "2026-03", "rate": 1.75}, {"date": "2026-05", "rate": 1.75}],
    "DUSD": [{"date": "2026-01", "rate": 5.00}, {"date": "2026-03", "rate": 4.75}, {"date": "2026-05", "rate": 4.50}],
}


async def get_current_rates() -> list[dict]:
    return [{"code": k, **v} for k, v in CBDC_RATES.items()]


async def get_rate(code: str) -> dict:
    info = CBDC_RATES.get(code.upper())
    if not info:
        return {"error": f"CBDC {code} not found"}
    return {"code": code.upper(), **info}


async def get_rate_history(code: str) -> list[dict]:
    return RATE_HISTORY.get(code.upper(), [])


async def project_interest(balance: float, code: str, days: int = 365) -> dict:
    info = CBDC_RATES.get(code.upper())
    if not info:
        return {"error": "Unknown CBDC"}
    rate = info["rate_pct"] / 100
    daily = balance * rate / 365
    yearly = balance * rate
    return {
        "cbdc": code.upper(), "balance": balance, "rate_pct": info["rate_pct"],
        "daily_interest": round(daily, 4), "monthly_interest": round(daily * 30, 4),
        "yearly_interest": round(yearly, 4), "projected_for_days": days,
        "total_projected": round(daily * days, 4),
    }
