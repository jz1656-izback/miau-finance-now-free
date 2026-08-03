"""Auto-generated Miau Finance Python SDK methods."""

from typing import Any, Optional


# --- analytics ---

    async def get_api_v1_analytics_summary(self):
        return await self._client.async_get("/api/v1/analytics/summary", params={})

    async def get_api_v1_analytics_monte-carlo(self, ticker: Optional[str] = None, num_simulations: Optional[str] = None, days: Optional[str] = None):
        return await self._client.async_get("/api/v1/analytics/monte-carlo", params={"ticker": ticker, "num_simulations": num_simulations, "days": days})

    async def get_api_v1_risk_var(self, ticker: Optional[str] = None, confidence: Optional[str] = None):
        return await self._client.async_get("/api/v1/risk/var", params={"ticker": ticker, "confidence": confidence})

    async def get_api_v1_risk_beta(self, ticker: Optional[str] = None, benchmark: Optional[str] = None):
        return await self._client.async_get("/api/v1/risk/beta", params={"ticker": ticker, "benchmark": benchmark})

    async def get_api_v1_risk_rolling(self, ticker: Optional[str] = None, window: Optional[str] = None, period: Optional[str] = None):
        return await self._client.async_get("/api/v1/risk/rolling", params={"ticker": ticker, "window": window, "period": period})


# --- billing ---

    async def get_api_v1_billing_subscription(self):
        return await self._client.async_get("/api/v1/billing/subscription", params={})

    async def get_api_v1_billing_usage(self):
        return await self._client.async_get("/api/v1/billing/usage", params={})

    async def get_api_v1_billing_invoices(self):
        return await self._client.async_get("/api/v1/billing/invoices", params={})


# --- developer ---

    async def get_api_v1_developer_dashboard(self):
        return await self._client.async_get("/api/v1/developer/dashboard", params={})

    async def get_api_v1_developer_api-keys(self):
        return await self._client.async_get("/api/v1/developer/api-keys", params={})

    async def post_api_v1_developer_api-keys_post(self):
        return await self._client.async_post("/api/v1/developer/api-keys", json=...)


# --- market ---

    async def get_api_v1_market_live(self, tickers: Optional[str] = None):
        return await self._client.async_get("/api/v1/market/live", params={"tickers": tickers})

    async def get_api_v1_market_historical(self, period: Optional[str] = None):
        return await self._client.async_get("/api/v1/market/historical/{ticker}", params={})

    async def get_api_v1_market_movers(self):
        return await self._client.async_get("/api/v1/market/movers", params={})

    async def get_api_v1_market_sectors(self):
        return await self._client.async_get("/api/v1/market/sectors", params={})

    async def get_api_v1_market_indicators(self):
        return await self._client.async_get("/api/v1/market/indicators", params={})

    async def get_api_v1_market_forex(self, base: Optional[str] = None):
        return await self._client.async_get("/api/v1/market/forex", params={"base": base})

    async def get_api_v1_market_crypto(self, coin: Optional[str] = None):
        return await self._client.async_get("/api/v1/market/crypto", params={"coin": coin})


# --- orders ---

    async def get_api_v1_orders(self):
        return await self._client.async_get("/api/v1/orders", params={})

    async def post_api_v1_orders_post(self):
        return await self._client.async_post("/api/v1/orders", json=...)

    async def get_api_v1_orders(self):
        return await self._client.async_get("/api/v1/orders/{id}", params={})


# --- portfolio ---

    async def get_api_v1_portfolios(self):
        return await self._client.async_get("/api/v1/portfolios", params={})

    async def post_api_v1_portfolios_post(self):
        return await self._client.async_post("/api/v1/portfolios", json=...)

    async def get_api_v1_portfolios(self):
        return await self._client.async_get("/api/v1/portfolios/{id}", params={})

    async def get_api_v1_portfolios_positions(self):
        return await self._client.async_get("/api/v1/portfolios/{id}/positions", params={})


    async def get_api_v1_portfolios_fx-pnl(self):
        return await self._client.async_get("/api/v1/portfolios/{id}/fx-pnl", params={})


# --- valuation ---

    async def get_api_v1_analytics_valuation_dcf(self, growth: Optional[str] = None, terminal_growth: Optional[str] = None, years: Optional[str] = None):
        return await self._client.async_get("/api/v1/analytics/valuation/dcf/{ticker}", params={})

    async def get_api_v1_analytics_valuation_wacc(self):
        return await self._client.async_get("/api/v1/analytics/valuation/wacc/{ticker}", params={})

    async def get_api_v1_analytics_valuation_comps(self):
        return await self._client.async_get("/api/v1/analytics/valuation/comps/{ticker}", params={})

    async def get_api_v1_analytics_valuation_lbo(self, debt: Optional[str] = None, exit_year: Optional[str] = None, exit_multiple: Optional[str] = None):
        return await self._client.async_get("/api/v1/analytics/valuation/lbo/{ticker}", params={})

