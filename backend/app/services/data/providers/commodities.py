"""Commodities provider — spot prices, petroleum, agricultural via Yahoo/FRED."""
import logging
from datetime import datetime, timezone
from app.services.data.base import DataSource, ProviderUnavailableError
from app.services.analytics._yf import get_price, get_info

logger = logging.getLogger(__name__)

COMMODITY_TICKERS: dict[str, dict] = {
    "GC=F": {"name": "Gold", "category": "Precious Metals", "unit": "USD/oz"},
    "SI=F": {"name": "Silver", "category": "Precious Metals", "unit": "USD/oz"},
    "PL=F": {"name": "Platinum", "category": "Precious Metals", "unit": "USD/oz"},
    "HG=F": {"name": "Copper", "category": "Industrial Metals", "unit": "USD/lb"},
    "CL=F": {"name": "Crude Oil (WTI)", "category": "Energy", "unit": "USD/bbl"},
    "BZ=F": {"name": "Brent Crude", "category": "Energy", "unit": "USD/bbl"},
    "NG=F": {"name": "Natural Gas", "category": "Energy", "unit": "USD/MMBtu"},
    "HO=F": {"name": "Heating Oil", "category": "Energy", "unit": "USD/gal"},
    "RB=F": {"name": "Gasoline (RBOB)", "category": "Energy", "unit": "USD/gal"},
    "ZC=F": {"name": "Corn", "category": "Agriculture", "unit": "USD/bu"},
    "ZW=F": {"name": "Wheat", "category": "Agriculture", "unit": "USD/bu"},
    "ZS=F": {"name": "Soybeans", "category": "Agriculture", "unit": "USD/bu"},
    "KC=F": {"name": "Coffee", "category": "Agriculture", "unit": "USD/lb"},
    "CC=F": {"name": "Cocoa", "category": "Agriculture", "unit": "USD/tonne"},
    "SB=F": {"name": "Sugar", "category": "Agriculture", "unit": "USD/lb"},
    "CT=F": {"name": "Cotton", "category": "Agriculture", "unit": "USD/lb"},
    "LE=F": {"name": "Live Cattle", "category": "Livestock", "unit": "USD/lb"},
    "HE=F": {"name": "Lean Hogs", "category": "Livestock", "unit": "USD/lb"},
    "PA=F": {"name": "Palladium", "category": "Precious Metals", "unit": "USD/oz"},
    "UX=F": {"name": "Uranium", "category": "Energy", "unit": "USD/lb"},
}

TUNA_TICKERS: dict[str, dict] = {
    "TUNA": {"name": "Premium Chunk Light Tuna (Can)", "category": "Cat Essentials", "unit": "USD/can"},
    "CATF": {"name": "Miau Cat Food Index", "category": "Cat Essentials", "unit": "USD"},
}


class CommoditiesProvider(DataSource):
    """Commodity spot prices via Yahoo Finance futures tickers."""

    @property
    def name(self) -> str:
        return "commodities"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def capabilities(self) -> list[str]:
        return ["commodities", "commodity_prices", "energy", "agriculture", "tuna"]

    async def _test_connection(self) -> bool:
        try:
            p = await get_price("GC=F")
            return p is not None and "price" in p
        except Exception:
            return False

    async def fetch_commodity(self, ticker: str) -> dict:
        ticker = ticker.upper()
        if not ticker.endswith("=F"):
            ticker = f"{ticker}=F"
        meta = COMMODITY_TICKERS.get(ticker, {"name": ticker, "category": "Other", "unit": ""})
        data = await get_price(ticker)
        if not data or "error" in data:
            raise ProviderUnavailableError(f"No data for commodity {ticker}")
        return {
            "ticker": ticker.replace("=F", ""),
            "name": meta["name"],
            "category": meta["category"],
            "unit": meta["unit"],
            "price": data.get("price", 0),
            "change": data.get("change", 0),
            "change_pct": data.get("change_pct", 0),
            "as_of": datetime.now(timezone.utc).isoformat(),
        }

    async def fetch_all_commodities(self) -> list[dict]:
        results = []
        for ticker, meta in COMMODITY_TICKERS.items():
            try:
                p = await get_price(ticker)
                if p and "price" in p:
                    results.append({
                        "ticker": ticker.replace("=F", ""),
                        "name": meta["name"],
                        "category": meta["category"],
                        "price": p.get("price", 0),
                        "change_pct": p.get("change_pct", 0),
                    })
            except Exception:
                continue
        return results

    async def fetch_by_category(self, category: str) -> list[dict]:
        results = []
        for ticker, meta in COMMODITY_TICKERS.items():
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

    async def fetch_tuna_price(self) -> dict:
        import random
        return {
            "name": "Premium Chunk Light Tuna (Can)",
            "price": round(random.uniform(1.50, 2.50), 2),
            "change_pct": round(random.uniform(-3, 3), 2),
            "unit": "USD/can",
            "as_of": datetime.now(timezone.utc).isoformat(),
            "cat_commentary": random.choice([
                "The cat approves of this tuna price.",
                "The purr-to-tuna ratio is looking favorable.",
                "🐟 Tuna is the only commodity that matters. Buy the dip.",
                "A can of tuna is the cat's unit of account.",
                "The Tuna-Bond spread is purring.",
            ]),
        }

    async def fetch_cat_food_index(self) -> list[dict]:
        import random
        items = [
            {"name": "Premium Chunk Light Tuna", "price": round(random.uniform(1.50, 2.80), 2), "change_pct": round(random.uniform(-2, 3), 2)},
            {"name": "Salmon Pate", "price": round(random.uniform(1.80, 3.20), 2), "change_pct": round(random.uniform(-1.5, 2.5), 2)},
            {"name": "Whitefish Medley", "price": round(random.uniform(1.60, 2.90), 2), "change_pct": round(random.uniform(-2.5, 4), 2)},
            {"name": "Chicken Dinner", "price": round(random.uniform(1.20, 2.40), 2), "change_pct": round(random.uniform(-1, 2), 2)},
            {"name": "Kitten Formula", "price": round(random.uniform(1.90, 3.50), 2), "change_pct": round(random.uniform(-3, 5), 2)},
        ]
        return items
