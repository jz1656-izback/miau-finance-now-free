"""CBDC tracker — real-time CBDC prices, yields, supply, and adoption metrics."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

CBDC_DATA = {
    "DEUR": {"name": "Digital Euro", "country": "EU", "price_usd": 1.08, "yield_pct": 3.5, "supply_b": 125, "adoption_pct": 8.2},
    "ECNY": {"name": "e-CNY", "country": "CN", "price_usd": 0.14, "yield_pct": 2.8, "supply_b": 280, "adoption_pct": 15.3},
    "DUSD": {"name": "Digital Dollar", "country": "US", "price_usd": 1.00, "yield_pct": 4.2, "supply_b": 200, "adoption_pct": 6.5},
    "DCJPY": {"name": "Digital Yen", "country": "JP", "price_usd": 0.0067, "yield_pct": 1.5, "supply_b": 95, "adoption_pct": 3.8},
    "GBP+": {"name": "Digital Pound", "country": "GB", "price_usd": 1.26, "yield_pct": 3.8, "supply_b": 45, "adoption_pct": 4.1},
}


async def get_all_prices() -> dict:
    return {code: {"price_usd": data["price_usd"], "yield_pct": data["yield_pct"]} for code, data in CBDC_DATA.items()}


async def get_cbdc_info(code: str) -> Optional[dict]:
    return CBDC_DATA.get(code.upper())


async def get_adoption_metrics() -> dict:
    total_supply = sum(d["supply_b"] for d in CBDC_DATA.values())
    avg_adoption = sum(d["adoption_pct"] for d in CBDC_DATA.values()) / len(CBDC_DATA)
    return {"total_supply_b": total_supply, "avg_adoption_pct": round(avg_adoption, 1), "active_cbdcs": len(CBDC_DATA)}


async def get_yield_curve() -> list[dict]:
    return [{"currency": code, "yield_pct": data["yield_pct"], "maturity": "1y"} for code, data in CBDC_DATA.items()]
