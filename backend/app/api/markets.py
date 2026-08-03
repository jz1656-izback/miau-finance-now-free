import logging
from datetime import timezone, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.market_hours import MarketHoursService, EXCHANGE_INFO

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/markets", tags=["Global Markets"])

MOCK_PRICES: dict[str, dict] = {
    "NYSE": {"last": 45218.32, "change": 0.82},
    "NASDAQ": {"last": 19842.56, "change": 1.14},
    "TSX": {"last": 22341.78, "change": -0.31},
    "LSE": {"last": 8321.45, "change": 0.53},
    "EURONEXT": {"last": 7892.11, "change": -0.12},
    "XETRA": {"last": 18456.90, "change": 0.67},
    "SIX": {"last": 12345.67, "change": 0.28},
    "TSE": {"last": 38762.15, "change": 1.45},
    "HKEX": {"last": 28765.40, "change": -0.89},
    "SSE": {"last": 3345.12, "change": 0.15},
    "NSE": {"last": 81234.56, "change": 0.92},
    "ASX": {"last": 7891.23, "change": -0.44},
    "B3": {"last": 127890.00, "change": 1.32},
    "BMV": {"last": 54321.78, "change": -0.67},
    "BCS": {"last": 6543.21, "change": 0.09},
    "MERVAL": {"last": 1782345.00, "change": 2.15},
    "DFM": {"last": 4321.56, "change": 0.11},
    "TADAWUL": {"last": 12345.90, "change": -0.23},
    "JSE": {"last": 76543.21, "change": 0.45},
}


def _get_market_status(exchange: str) -> dict:
    info = EXCHANGE_INFO.get(exchange, {})
    now = datetime.now()
    mh = MarketHoursService.market_hours(exchange, now)
    prices = MOCK_PRICES.get(exchange, {"last": 0, "change": 0})
    is_open = mh.is_open if mh else False
    return {
        "exchange": exchange,
        "name": info.get("name", exchange),
        "country": info.get("country", ""),
        "timezone": info.get("tz", "UTC"),
        "local_time": now.astimezone().isoformat() if now.tzinfo else now.isoformat(),
        "open_time": str(mh.open_time) if mh and mh.open_time else None,
        "close_time": str(mh.close_time) if mh and mh.close_time else None,
        "is_open": is_open,
        "next_open": mh.next_open.isoformat() if mh and mh.next_open else None,
        "last_price": prices["last"],
        "change_pct": prices["change"],
        "status": "open" if mh.is_open else "closed",
    }


@router.get("/global")
async def global_markets():
    exchanges = []
    for code in sorted(EXCHANGE_INFO.keys()):
        exchanges.append(_get_market_status(code))
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_exchanges": len(exchanges),
        "open_count": sum(1 for e in exchanges if e["is_open"]),
        "exchanges": exchanges,
    }


@router.get("/global/{exchange}")
async def exchange_detail(exchange: str):
    code = exchange.upper()
    if code not in EXCHANGE_INFO:
        raise HTTPException(404, f"Unknown exchange: {exchange}")
    return _get_market_status(code)
