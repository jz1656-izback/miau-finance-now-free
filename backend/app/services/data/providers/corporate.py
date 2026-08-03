"""Corporate HQ provider — Fortune 2000+ companies with lat/lng, industry, revenue."""

import logging
from typing import Any, Optional

from app.services.data.base import DataSource

logger = logging.getLogger(__name__)

FORTUNE_COMPANIES: list[dict[str, Any]] = [
    {"name": "Walmart", "ticker": "WMT", "lat": 36.363, "lng": -94.215, "industry": "Retail", "revenue_b": 611.0},
    {"name": "Amazon", "ticker": "AMZN", "lat": 47.615, "lng": -122.339, "industry": "E-Commerce", "revenue_b": 574.0},
    {"name": "Apple", "ticker": "AAPL", "lat": 37.336, "lng": -122.007, "industry": "Technology", "revenue_b": 383.0},
    {"name": "Berkshire Hathaway", "ticker": "BRK.A", "lat": 41.256, "lng": -95.934, "industry": "Conglomerate", "revenue_b": 364.0},
    {"name": "Alphabet", "ticker": "GOOGL", "lat": 37.422, "lng": -122.084, "industry": "Technology", "revenue_b": 307.0},
    {"name": "Microsoft", "ticker": "MSFT", "lat": 47.640, "lng": -122.129, "industry": "Technology", "revenue_b": 211.0},
    {"name": "Saudi Aramco", "ticker": "2222.SR", "lat": 25.261, "lng": 50.214, "industry": "Energy", "revenue_b": 494.0},
    {"name": "Toyota", "ticker": "TM", "lat": 35.052, "lng": 137.155, "industry": "Automotive", "revenue_b": 275.0},
    {"name": "Samsung", "ticker": "005930.KS", "lat": 37.479, "lng": 127.020, "industry": "Technology", "revenue_b": 244.0},
    {"name": "JPMorgan Chase", "ticker": "JPM", "lat": 40.754, "lng": -73.973, "industry": "Banking", "revenue_b": 169.0},
    {"name": "Tencent", "ticker": "TCEHY", "lat": 22.543, "lng": 113.953, "industry": "Technology", "revenue_b": 86.0},
    {"name": "Nvidia", "ticker": "NVDA", "lat": 37.395, "lng": -121.964, "industry": "Semiconductors", "revenue_b": 79.0},
    {"name": "Tesla", "ticker": "TSLA", "lat": 30.223, "lng": -97.620, "industry": "Automotive", "revenue_b": 96.0},
    {"name": "Nestlé", "ticker": "NSRGY", "lat": 46.519, "lng": 6.632, "industry": "Food", "revenue_b": 104.0},
    {"name": "Meta", "ticker": "META", "lat": 37.485, "lng": -122.149, "industry": "Technology", "revenue_b": 134.0},
    {"name": "ExxonMobil", "ticker": "XOM", "lat": 32.756, "lng": -97.308, "industry": "Energy", "revenue_b": 344.0},
    {"name": "LVMH", "ticker": "MC.PA", "lat": 48.870, "lng": 2.321, "industry": "Luxury", "revenue_b": 86.0},
    {"name": "Siemens", "ticker": "SIE.DE", "lat": 48.169, "lng": 11.615, "industry": "Industrial", "revenue_b": 72.0},
    {"name": "Shell", "ticker": "SHEL", "lat": 52.077, "lng": 4.310, "industry": "Energy", "revenue_b": 323.0},
    {"name": "Volkswagen", "ticker": "VOW3.DE", "lat": 52.433, "lng": 10.779, "industry": "Automotive", "revenue_b": 295.0},
    {"name": "ICBC", "ticker": "1398.HK", "lat": 39.909, "lng": 116.360, "industry": "Banking", "revenue_b": 208.0},
    {"name": "Alibaba", "ticker": "BABA", "lat": 30.274, "lng": 120.155, "industry": "E-Commerce", "revenue_b": 126.0},
    {"name": "BNP Paribas", "ticker": "BNP.PA", "lat": 48.876, "lng": 2.333, "industry": "Banking", "revenue_b": 91.0},
    {"name": "Visa", "ticker": "V", "lat": 37.558, "lng": -122.280, "industry": "Finance", "revenue_b": 33.0},
    {"name": "Rio Tinto", "ticker": "RIO", "lat": 51.507, "lng": -0.083, "industry": "Mining", "revenue_b": 54.0},
    {"name": "BHP", "ticker": "BHP", "lat": -37.830, "lng": 144.982, "industry": "Mining", "revenue_b": 65.0},
    {"name": "Mitsubishi", "ticker": "8058.T", "lat": 35.676, "lng": 139.773, "industry": "Conglomerate", "revenue_b": 148.0},
    {"name": "TotalEnergies", "ticker": "TTE", "lat": 48.876, "lng": 2.333, "industry": "Energy", "revenue_b": 237.0},
    {"name": "UnitedHealth", "ticker": "UNH", "lat": 39.744, "lng": -105.010, "industry": "Healthcare", "revenue_b": 371.0},
    {"name": "HSBC", "ticker": "HSBC", "lat": 51.507, "lng": -0.083, "industry": "Banking", "revenue_b": 75.0},
    {"name": "PetroChina", "ticker": "PTR", "lat": 39.908, "lng": 116.431, "industry": "Energy", "revenue_b": 358.0},
    {"name": "Airbus", "ticker": "AIR.PA", "lat": 43.626, "lng": 1.368, "industry": "Aerospace", "revenue_b": 66.0},
    {"name": "SAP", "ticker": "SAP", "lat": 49.293, "lng": 8.640, "industry": "Technology", "revenue_b": 34.0},
    {"name": "Vale", "ticker": "VALE", "lat": -22.909, "lng": -43.179, "industry": "Mining", "revenue_b": 45.0},
    {"name": "Anheuser-Busch InBev", "ticker": "BUD", "lat": 50.854, "lng": 4.366, "industry": "Food", "revenue_b": 59.0},
    {"name": "Adidas", "ticker": "ADS.DE", "lat": 49.757, "lng": 10.900, "industry": "Consumer", "revenue_b": 23.0},
    {"name": "L'Oréal", "ticker": "OR.PA", "lat": 48.876, "lng": 2.304, "industry": "Consumer", "revenue_b": 43.0},
    {"name": "Mitsui", "ticker": "8031.T", "lat": 35.676, "lng": 139.773, "industry": "Conglomerate", "revenue_b": 114.0},
    {"name": "Oracle", "ticker": "ORCL", "lat": 37.528, "lng": -122.262, "industry": "Technology", "revenue_b": 50.0},
    {"name": "Cisco", "ticker": "CSCO", "lat": 37.397, "lng": -121.961, "industry": "Technology", "revenue_b": 52.0},
    {"name": "PepsiCo", "ticker": "PEP", "lat": 41.136, "lng": -73.725, "industry": "Food", "revenue_b": 91.0},
    {"name": "Mastercard", "ticker": "MA", "lat": 41.136, "lng": -73.759, "industry": "Finance", "revenue_b": 25.0},
]


class CorporateDataSource(DataSource):
    """Fortune global HQ locations with industry classification."""

    @property
    def name(self) -> str:
        return "corporate"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 1000

    @property
    def capabilities(self) -> list[str]:
        return ["globe_corporate", "corporate_data"]

    async def _test_connection(self) -> bool:
        return len(FORTUNE_COMPANIES) > 0

    async def fetch_quote(self, ticker: str) -> dict:
        return {"error": "Not applicable — corporate data source does not provide quotes"}

    async def fetch(self, query: Optional[str] = None, **kwargs) -> dict[str, Any]:
        industry = kwargs.get("industry")
        if industry:
            companies = [c for c in FORTUNE_COMPANIES if c["industry"] == industry]
        else:
            companies = list(FORTUNE_COMPANIES)
        return {"companies": companies, "count": len(companies)}

    async def fetch_globe_corporate(self, industry: Optional[str] = None) -> dict[str, Any]:
        return await self.fetch(industry=industry)


data_source = CorporateDataSource()
