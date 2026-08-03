"""Frankfurter API — live/historical FX rates for 200+ currencies, 55 central banks."""
import logging
import time
import httpx
from datetime import datetime
from typing import Optional
from app.services.data.base import DataSource
from app.services.data.models import FXRate

logger = logging.getLogger(__name__)


class FrankfurterProvider(DataSource):
    """Free FX rates from Frankfurter.app. No key, no rate limits."""

    @property
    def name(self) -> str:
        return "frankfurter"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 9999

    @property
    def base_url(self) -> str:
        return "https://api.frankfurter.app"

    @property
    def capabilities(self) -> list[str]:
        return ["fx"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}/latest?base=USD")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_fx_rates(self, base: str = "USD") -> dict[str, float]:
        start = time.monotonic()
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/latest?base={base.upper()}")
            elapsed = round((time.monotonic() - start) * 1000, 1)
            if r.status_code != 200:
                logger.warning("Frankfurter %s returned %d (%sms)", base, r.status_code, elapsed)
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Frankfurter returned {r.status_code}")
            logger.debug("Frankfurter %s OK (%sms)", base, elapsed)
            data = r.json()
            rates = {str(k): float(v) for k, v in data.get("rates", {}).items()}
            rates[base.upper()] = 1.0
            return rates

    async def fetch_fx_convert(self, amount: float, from_currency: str, to_currency: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/latest?base={from_currency.upper()}&symbols={to_currency.upper()}")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Frankfurter returned {r.status_code}")
            data = r.json()
            rate = float(data.get("rates", {}).get(to_currency.upper(), 0))
            result = amount * rate
            return {
                "amount": amount,
                "from": from_currency.upper(),
                "to": to_currency.upper(),
                "rate": rate,
                "result": round(result, 2),
                "date": data.get("date", ""),
            }

    async def fetch_fx_history(self, base: str, target: str, from_date: str, to_date: Optional[str] = None) -> list[FXRate]:
        end = to_date or "latest"
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/{from_date}..{end}?base={base.upper()}&symbols={target.upper()}")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Frankfurter returned {r.status_code}")
            data = r.json()
            rates = data.get("rates", {})
            results = []
            for date_str in sorted(rates.keys()):
                rate_dict = rates[date_str]
                if target.upper() in rate_dict:
                    results.append(FXRate(base=base.upper(), target=target.upper(), rate=float(rate_dict[target.upper()]), date=date_str))
            return results
