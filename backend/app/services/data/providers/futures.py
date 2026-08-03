"""Futures provider — futures curves, contract specs, historical data via Yahoo."""
import logging
from datetime import datetime, timezone
from app.services.data.base import DataSource, ProviderUnavailableError
from app.services.analytics._yf import get_price

logger = logging.getLogger(__name__)

FUTURES_SYMBOLS: dict[str, dict] = {
    "ES=F": {"name": "S&P 500 E-mini", "exchange": "CME", "category": "Equity Index"},
    "NQ=F": {"name": "Nasdaq 100 E-mini", "exchange": "CME", "category": "Equity Index"},
    "YM=F": {"name": "Dow Jones E-mini", "exchange": "CBOT", "category": "Equity Index"},
    "RTY=F": {"name": "Russell 2000 E-mini", "exchange": "CME", "category": "Equity Index"},
    "CL=F": {"name": "Crude Oil (WTI)", "exchange": "NYMEX", "category": "Energy"},
    "BZ=F": {"name": "Brent Crude", "exchange": "ICE", "category": "Energy"},
    "NG=F": {"name": "Natural Gas", "exchange": "NYMEX", "category": "Energy"},
    "GC=F": {"name": "Gold", "exchange": "COMEX", "category": "Metals"},
    "SI=F": {"name": "Silver", "exchange": "COMEX", "category": "Metals"},
    "HG=F": {"name": "Copper", "exchange": "COMEX", "category": "Metals"},
    "ZC=F": {"name": "Corn", "exchange": "CBOT", "category": "Agriculture"},
    "ZW=F": {"name": "Wheat", "exchange": "CBOT", "category": "Agriculture"},
    "ZS=F": {"name": "Soybeans", "exchange": "CBOT", "category": "Agriculture"},
    "6E=F": {"name": "Euro FX", "exchange": "CME", "category": "Currency"},
    "6B=F": {"name": "British Pound", "exchange": "CME", "category": "Currency"},
    "6J=F": {"name": "Japanese Yen", "exchange": "CME", "category": "Currency"},
    "ZB=F": {"name": "US Treasury Bond", "exchange": "CBOT", "category": "Interest Rate"},
    "ZN=F": {"name": "10-Year T-Note", "exchange": "CBOT", "category": "Interest Rate"},
    "ZF=F": {"name": "5-Year T-Note", "exchange": "CBOT", "category": "Interest Rate"},
    "ZT=F": {"name": "2-Year T-Note", "exchange": "CBOT", "category": "Interest Rate"},
}


class FuturesProvider(DataSource):
    """Futures data — prices, contract specs, categories via Yahoo."""

    @property
    def name(self) -> str:
        return "futures"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def capabilities(self) -> list[str]:
        return ["futures", "futures_prices", "derivatives"]

    async def _test_connection(self) -> bool:
        try:
            p = await get_price("ES=F")
            return p is not None and "price" in p
        except Exception:
            return False

    async def fetch_future(self, ticker: str) -> dict:
        ticker = ticker.upper()
        if not ticker.endswith("=F"):
            ticker = f"{ticker}=F"
        meta = FUTURES_SYMBOLS.get(ticker, {"name": ticker, "exchange": "", "category": "Other"})
        data = await get_price(ticker)
        if not data or "error" in data:
            raise ProviderUnavailableError(f"No data for future {ticker}")
        return {
            "ticker": ticker.replace("=F", ""),
            "name": meta["name"],
            "exchange": meta["exchange"],
            "category": meta["category"],
            "price": data.get("price", 0),
            "change": data.get("change", 0),
            "change_pct": data.get("change_pct", 0),
            "volume": data.get("volume", 0),
            "as_of": datetime.now(timezone.utc).isoformat(),
        }

    async def fetch_all_futures(self) -> list[dict]:
        results = []
        for ticker, meta in FUTURES_SYMBOLS.items():
            try:
                p = await get_price(ticker)
                if p and "price" in p:
                    results.append({
                        "ticker": ticker.replace("=F", ""),
                        "name": meta["name"],
                        "category": meta["category"],
                        "exchange": meta["exchange"],
                        "price": p.get("price", 0),
                        "change_pct": p.get("change_pct", 0),
                    })
            except Exception:
                continue
        return results

    async def fetch_by_category(self, category: str) -> list[dict]:
        results = []
        for ticker, meta in FUTURES_SYMBOLS.items():
            if meta["category"].lower() == category.lower():
                try:
                    p = await get_price(ticker)
                    if p and "price" in p:
                        results.append({
                            "ticker": ticker.replace("=F", ""),
                            "name": meta["name"],
                            "price": p.get("price", 0),
                            "change_pct": p.get("change_pct", 0),
                        })
                except Exception:
                    continue
        return results
