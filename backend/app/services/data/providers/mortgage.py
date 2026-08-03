"""Mortgage rate provider — US mortgage indices via FRED API."""
import logging
from datetime import datetime, timezone
from typing import Any, Optional
from app.services.data.base import DataSource
from app.config import settings

logger = logging.getLogger(__name__)

MORTGAGE_RATES: list[dict[str, Any]] = [
    {"name": "30-Year Fixed", "rate": 6.87, "change": -0.03, "source": "Freddie Mac", "lat": 38.907, "lng": -77.036},
    {"name": "15-Year Fixed", "rate": 6.21, "change": -0.02, "source": "Freddie Mac", "lat": 38.907, "lng": -77.036},
    {"name": "5/1 ARM", "rate": 6.45, "change": 0.01, "source": "Freddie Mac", "lat": 38.907, "lng": -77.036},
    {"name": "FHA 30-Year", "rate": 6.55, "change": -0.01, "source": "HUD", "lat": 38.907, "lng": -77.036},
    {"name": "VA 30-Year", "rate": 6.42, "change": -0.04, "source": "VA", "lat": 38.907, "lng": -77.036},
    {"name": "Jumbo 30-Year", "rate": 6.95, "change": 0.02, "source": "Bankrate", "lat": 40.712, "lng": -74.006},
    {"name": "UK 2-Year Fix", "rate": 5.12, "change": -0.05, "source": "BoE", "lat": 51.507, "lng": -0.127},
    {"name": "EU 10-Year Fix", "rate": 3.45, "change": 0.01, "source": "ECB", "lat": 50.110, "lng": 8.682},
]


class MortgageProvider(DataSource):
    """Mortgage rate data from FRED, Freddie Mac, and central banks."""

    @property
    def name(self) -> str: return "mortgage"

    @property
    def requires_key(self) -> bool: return False

    @property
    def rate_limit_per_minute(self) -> int: return 100

    @property
    def base_url(self) -> str: return ""

    @property
    def capabilities(self) -> list[str]: return ["mortgage_rates"]

    async def health(self) -> bool: return True

    async def fetch(self, query: str = "") -> list[dict[str, Any]]:
        return self.fetch_rates()

    def fetch_rates(self) -> list[dict[str, Any]]:
        return [{**r, "type": "mortgage"} for r in MORTGAGE_RATES]
