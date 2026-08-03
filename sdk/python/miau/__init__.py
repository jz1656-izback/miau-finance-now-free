"""Miau Finance Python SDK."""
from __future__ import annotations
import os
from typing import Any, Optional

class MiauError(Exception):
    def __init__(self, status: int, message: str, body: Any = None):
        self.status = status; self.body = body; super().__init__(f"[{status}] {message}")

class MiauAuthError(MiauError): pass
class MiauRateLimitError(MiauError): pass

class MiauClient:
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://miau.finance/api/v1", timeout: int = 30):
        self.api_key = api_key or os.getenv("MIAU_API_KEY", ""); self.base_url = base_url.rstrip("/"); self.timeout = timeout

    @property
    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json", "Accept": "application/json"}

    def _request(self, method, path, params=None, json_body=None):
        import requests
        resp = requests.request(method.upper(), f"{self.base_url}/{path.lstrip('/')}", headers=self._headers, params=params, json=json_body, timeout=self.timeout)
        if resp.status_code == 401: raise MiauAuthError(401, "Invalid API key")
        if resp.status_code == 403: raise MiauAuthError(403, "Forbidden")
        if resp.status_code == 429: raise MiauRateLimitError(429, f"Rate limited")
        if not resp.ok: raise MiauError(resp.status_code, f"Failed: {resp.reason}", resp.text)
        return resp.json() if resp.status_code != 204 else None

    @property
    def market(self):
        from miau.market import MarketModule; return MarketModule(self)
    @property
    def portfolio(self):
        from miau.portfolio import PortfolioModule; return PortfolioModule(self)
    @property
    def trading(self):
        from miau.trading import TradingModule; return TradingModule(self)
