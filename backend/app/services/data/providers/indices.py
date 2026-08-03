"""Index data provider — major market indices, constituents, performance via Yahoo."""
import logging
from datetime import datetime, timezone
from app.services.data.base import DataSource, ProviderUnavailableError
from app.services.analytics._yf import get_price, get_info

logger = logging.getLogger(__name__)

MAJOR_INDICES: dict[str, dict] = {
    "^GSPC": {"name": "S&P 500", "alias": "SPX", "country": "US"},
    "^DJI": {"name": "Dow Jones Industrial Average", "alias": "DJIA", "country": "US"},
    "^IXIC": {"name": "Nasdaq Composite", "alias": "COMP", "country": "US"},
    "^RUT": {"name": "Russell 2000", "alias": "RUT", "country": "US"},
    "^VIX": {"name": "CBOE Volatility Index", "alias": "VIX", "country": "US"},
    "^FTSE": {"name": "FTSE 100", "alias": "UK100", "country": "UK"},
    "^N225": {"name": "Nikkei 225", "alias": "NKY", "country": "Japan"},
    "^HSI": {"name": "Hang Seng Index", "alias": "HSI", "country": "Hong Kong"},
    "^STOXX50E": {"name": "Euro STOXX 50", "alias": "SX5E", "country": "Eurozone"},
    "^AXJO": {"name": "ASX 200", "alias": "AS51", "country": "Australia"},
    "^KS11": {"name": "KOSPI Composite", "alias": "KOSPI", "country": "South Korea"},
    "^BSESN": {"name": "BSE Sensex", "alias": "SENSEX", "country": "India"},
    "^BVSP": {"name": "IBOVESPA", "alias": "IBOV", "country": "Brazil"},
    "^GDAXI": {"name": "DAX Performance", "alias": "DAX", "country": "Germany"},
    "^FCHI": {"name": "CAC 40", "alias": "CAC", "country": "France"},
    "^SSMI": {"name": "Swiss Market Index", "alias": "SMI", "country": "Switzerland"},
    "^TSEC": {"name": "Taiwan Weighted", "alias": "TWII", "country": "Taiwan"},
    "^KQ11": {"name": "KOSDAQ", "alias": "KOSDAQ", "country": "South Korea"},
    "^IPSA": {"name": "IPSA", "alias": "IPSA", "country": "Chile"},
    "^MXX": {"name": "IPC Mexico", "alias": "MEXBOL", "country": "Mexico"},
}


class IndexProvider(DataSource):
    """Major market indices — quotes, performance, global coverage."""

    @property
    def name(self) -> str:
        return "indices"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def base_url(self) -> str:
        return "https://query1.finance.yahoo.com"

    @property
    def capabilities(self) -> list[str]:
        return ["indices", "index_quotes", "global_markets"]

    async def _test_connection(self) -> bool:
        try:
            p = await get_price("^GSPC")
            return p is not None and "price" in p
        except Exception:
            return False

    async def fetch_index_list(self) -> list[dict]:
        return [
            {"ticker": t, "name": v["name"], "alias": v["alias"], "country": v["country"]}
            for t, v in MAJOR_INDICES.items()
        ]

    async def fetch_index_quote(self, ticker: str) -> dict:
        ticker = ticker.upper()
        if not ticker.startswith("^"):
            # Accept both ^GSPC and SPX alias
            for k, v in MAJOR_INDICES.items():
                if v["alias"] == ticker or k == f"^{ticker}":
                    ticker = k
                    break
        data = await get_price(ticker)
        if not data or "error" in data:
            raise ProviderUnavailableError(f"No data for index {ticker}")
        meta = MAJOR_INDICES.get(ticker, {"name": ticker, "country": "Unknown"})
        info = await get_info(ticker)
        return {
            "ticker": meta.get("alias", ticker),
            "name": meta["name"],
            "country": meta.get("country", "Unknown"),
            "price": data.get("price", 0),
            "change": data.get("change", 0),
            "change_pct": data.get("change_pct", 0),
            "volume": data.get("volume", 0),
            "prev_close": info.get("summaryDetail", {}).get("previousClose", {}).get("raw"),
            "52w_high": info.get("summaryDetail", {}).get("fiftyTwoWeekHigh", {}).get("raw"),
            "52w_low": info.get("summaryDetail", {}).get("fiftyTwoWeekLow", {}).get("raw"),
            "as_of": datetime.now(timezone.utc).isoformat(),
        }

    async def fetch_all_indices(self) -> list[dict]:
        results = []
        for ticker in MAJOR_INDICES:
            try:
                p = await get_price(ticker)
                if p and "price" in p:
                    meta = MAJOR_INDICES[ticker]
                    results.append({
                        "ticker": meta["alias"],
                        "name": meta["name"],
                        "country": meta["country"],
                        "price": p.get("price", 0),
                        "change_pct": p.get("change_pct", 0),
                    })
            except Exception:
                continue
        results.sort(key=lambda x: abs(x["change_pct"]), reverse=True)
        return results
