"""ETF data provider — sector ETFs, holdings, performance via Yahoo Finance."""
import logging
from datetime import datetime, timezone
from app.services.data.base import DataSource, ProviderUnavailableError
from app.services.data.providers.yahoo import YahooProvider
from app.services.analytics._yf import get_price, get_info, fetch_sector_etfs

logger = logging.getLogger(__name__)

MAJOR_ETFS: dict[str, str] = {
    "SPY": "SPDR S&P 500 ETF",
    "QQQ": "Invesco QQQ Trust (Nasdaq 100)",
    "IVV": "iShares Core S&P 500",
    "VOO": "Vanguard S&P 500 ETF",
    "VTI": "Vanguard Total Stock Market",
    "BND": "Vanguard Total Bond Market",
    "AGG": "iShares Core US Aggregate Bond",
    "GLD": "SPDR Gold Shares",
    "IWM": "iShares Russell 2000",
    "EEM": "iShares MSCI Emerging Markets",
    "EFA": "iShares MSCI EAFE (Developed ex-US)",
    "VNQ": "Vanguard Real Estate",
    "XLF": "Financials Select Sector",
    "XLK": "Technology Select Sector",
    "XLE": "Energy Select Sector",
    "XLV": "Healthcare Select Sector",
    "TLT": "iShares 20+ Year Treasury Bond",
    "SHY": "iShares 1-3 Year Treasury Bond",
    "LQD": "iShares Investment Grade Corporate Bond",
    "HYG": "iShares High Yield Corporate Bond",
    "ARKK": "ARK Innovation ETF",
    "VXUS": "Vanguard Total International Stock",
    "VUG": "Vanguard Growth ETF",
    "VTV": "Vanguard Value ETF",
    "SCHD": "Schwab US Dividend Equity ETF",
}


class ETFProvider(DataSource):
    """ETF data via Yahoo Finance — quotes, sectors, holdings, performance."""

    @property
    def name(self) -> str:
        return "etf"

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
        return ["etf", "etf_quote", "etf_sectors", "etf_holdings", "etf_performance"]

    async def _test_connection(self) -> bool:
        try:
            p = await get_price("SPY")
            return p is not None and "price" in p
        except Exception:
            return False

    async def fetch_etf_list(self) -> list[dict]:
        return [{"ticker": t, "name": n} for t, n in MAJOR_ETFS.items()]

    async def fetch_etf_quote(self, ticker: str) -> dict:
        ticker = ticker.upper()
        data = await get_price(ticker)
        if not data or "error" in data:
            raise ProviderUnavailableError(f"No data for ETF {ticker}")
        info = await get_info(ticker)
        name = MAJOR_ETFS.get(ticker, info.get("price", {}).get("longName", ticker))
        return {
            "ticker": ticker,
            "name": name,
            "price": data.get("price", 0),
            "change": data.get("change", 0),
            "change_pct": data.get("change_pct", 0),
            "volume": data.get("volume", 0),
            "nav": info.get("summaryDetail", {}).get("navPrice", {}).get("raw"),
            "yield_pct": info.get("summaryDetail", {}).get("yield", {}).get("raw"),
            "beta": info.get("defaultKeyStatistics", {}).get("beta", {}).get("raw"),
            "category": info.get("assetProfile", {}).get("category"),
            "fund_family": info.get("assetProfile", {}).get("fundFamily"),
            "as_of": datetime.now(timezone.utc).isoformat(),
        }

    async def fetch_sector_performance(self) -> dict:
        return await fetch_sector_etfs()

    async def fetch_top_etfs(self, limit: int = 10) -> list[dict]:
        results = []
        for ticker in list(MAJOR_ETFS.keys())[:limit]:
            try:
                p = await get_price(ticker)
                if p and "price" in p:
                    results.append({
                        "ticker": ticker,
                        "name": MAJOR_ETFS[ticker],
                        "price": p.get("price", 0),
                        "change_pct": p.get("change_pct", 0),
                    })
            except Exception:
                continue
        return results
