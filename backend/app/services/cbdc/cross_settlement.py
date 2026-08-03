import logging
from typing import Optional

logger = logging.getLogger(__name__)

SUPPORTED_CBDCS = {
    "DEUR": {"name": "Digital Euro", "country": "EU", "min_settlement": 100, "max_settlement": 10000000},
    "ECNY": {"name": "Digital Yuan", "country": "CN", "min_settlement": 50, "max_settlement": 5000000},
    "DUSD": {"name": "Digital Dollar", "country": "US", "min_settlement": 100, "max_settlement": 20000000},
    "DCJPY": {"name": "Digital Yen", "country": "JP", "min_settlement": 5000, "max_settlement": 500000000},
    "GBP+": {"name": "Digital Pound", "country": "GB", "min_settlement": 100, "max_settlement": 10000000},
}

EXCHANGE_RATES = {
    "DEUR": {"DUSD": 1.08, "GBP+": 0.86, "DCJPY": 162.5, "ECNY": 7.85},
    "ECNY": {"DEUR": 0.13, "DUSD": 0.14, "GBP+": 0.11, "DCJPY": 21.8},
    "DUSD": {"DEUR": 0.93, "ECNY": 7.24, "GBP+": 0.79, "DCJPY": 151.0},
    "DCJPY": {"DEUR": 0.0062, "DUSD": 0.0066, "GBP+": 0.0052, "ECNY": 0.047},
    "GBP+": {"DEUR": 1.16, "DUSD": 1.26, "ECNY": 9.15, "DCJPY": 190.8},
}


async def list_cbdcs() -> list[dict]:
    return [{"code": k, **v} for k, v in SUPPORTED_CBDCS.items()]


async def get_rate(from_cbdc: str, to_cbdc: str) -> float:
    rates = EXCHANGE_RATES.get(from_cbdc.upper(), {})
    return rates.get(to_cbdc.upper(), 1.0)


async def settle(from_cbdc: str, to_cbdc: str, amount: float) -> dict:
    from_info = SUPPORTED_CBDCS.get(from_cbdc.upper())
    to_info = SUPPORTED_CBDCS.get(to_cbdc.upper())
    if not from_info or not to_info:
        return {"error": "Unsupported CBDC"}
    rate = await get_rate(from_cbdc, to_cbdc)
    fee_pct = 0.002
    fee = amount * fee_pct
    converted = amount * rate
    return {
        "from": from_cbdc, "to": to_cbdc, "amount": amount,
        "rate": rate, "fee": round(fee, 2), "converted": round(converted, 2),
        "settlement_time": "2-10 min", "corridor": f"{from_info['country']} → {to_info['country']}",
    }


async def get_corridor_volume(from_cbdc: str, to_cbdc: str) -> dict:
    volumes = {
        ("DEUR", "DUSD"): {"daily": "€420M", "monthly": "€12.8B", "trend": "growing"},
        ("ECNY", "DUSD"): {"daily": "¥2.1B", "monthly": "¥58B", "trend": "growing"},
        ("DEUR", "GBP+"): {"daily": "€180M", "monthly": "€5.2B", "trend": "stable"},
    }
    return volumes.get((from_cbdc.upper(), to_cbdc.upper()), {"daily": "N/A", "monthly": "N/A", "trend": "unknown"})
