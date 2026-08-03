import asyncio
import logging
import time
from typing import AsyncGenerator, Callable, Optional

import httpx

logger = logging.getLogger(__name__)


class MarketDataStream:
    def __init__(self, broker_endpoint: str, api_key: str, reconnect_delay: float = 5.0):
        self._endpoint = broker_endpoint.rstrip("/")
        self._api_key = api_key
        self._reconnect_delay = reconnect_delay
        self._client: Optional[httpx.AsyncClient] = None
        self._running = False
        self._subscribed: set[str] = set()
        self._latest_prices: dict[str, float] = {}
        self._callbacks: list[Callable[[str, float], None]] = []

    def on_price(self, callback: Callable[[str, float], None]) -> None:
        self._callbacks.append(callback)

    def get_latest_price(self, ticker: str) -> Optional[float]:
        return self._latest_prices.get(ticker.upper())

    def get_all_prices(self) -> dict[str, float]:
        return dict(self._latest_prices)

    async def connect(self) -> "MarketDataStream":
        self._client = httpx.AsyncClient(
            base_url=self._endpoint,
            headers={"Authorization": f"Bearer {self._api_key}"},
            timeout=30.0,
        )
        self._running = True
        logger.info(f"Connected to market data stream at {self._endpoint}")
        return self

    async def disconnect(self) -> None:
        self._running = False
        if self._client:
            await self._client.aclose()
            self._client = None
        logger.info("Disconnected from market data stream")

    async def subscribe(self, tickers: list[str]) -> None:
        for t in tickers:
            self._subscribed.add(t.upper())
        logger.info(f"Subscribed to {len(tickers)} tickers: {tickers}")

    async def unsubscribe(self, ticker: str) -> None:
        self._subscribed.discard(ticker.upper())

    async def stream(self, tickers: list[str], interval: float = 1.0) -> AsyncGenerator[dict[str, float], None]:
        await self.connect()
        await self.subscribe(tickers)
        seen: dict[str, float] = {}
        while self._running:
            try:
                if not self._subscribed:
                    await asyncio.sleep(interval)
                    continue
                tickers_str = ",".join(self._subscribed)
                resp = await self._client.get(f"/v1/market/live?tickers={tickers_str}")
                if resp.status_code == 200:
                    data = resp.json()
                    update: dict[str, float] = {}
                    for ticker, info in data.get("data", {}).items():
                        price = info.get("price")
                        if price is not None:
                            p = float(price)
                            key = ticker.upper()
                            self._latest_prices[key] = p
                            if key not in seen or seen[key] != p:
                                seen[key] = p
                                update[key] = p
                            for cb in self._callbacks:
                                cb(key, p)
                    if update:
                        yield update
            except httpx.RequestError as e:
                logger.warning(f"Poll failed: {e}")
                await self._reconnect()
            except Exception as e:
                logger.error(f"Unexpected poll error: {e}")
            await asyncio.sleep(interval)
        await self.disconnect()

    async def poll_prices(self, interval: float = 1.0) -> None:
        while self._running:
            if not self._subscribed:
                await asyncio.sleep(interval)
                continue
            try:
                tickers_str = ",".join(self._subscribed)
                resp = await self._client.get(f"/v1/market/live?tickers={tickers_str}")
                if resp.status_code == 200:
                    data = resp.json()
                    for ticker, info in data.get("data", {}).items():
                        price = info.get("price")
                        if price is not None:
                            p = float(price)
                            self._latest_prices[ticker.upper()] = p
                            for cb in self._callbacks:
                                cb(ticker.upper(), p)
            except httpx.RequestError as e:
                logger.warning(f"Poll failed: {e}")
                await self._reconnect()
            except Exception as e:
                logger.error(f"Unexpected poll error: {e}")
            await asyncio.sleep(interval)

    async def _reconnect(self) -> None:
        logger.info(f"Reconnecting in {self._reconnect_delay}s...")
        await self.disconnect()
        await asyncio.sleep(self._reconnect_delay)
        await self.connect()

    async def start_streaming(self, tickers: list[str], interval: float = 1.0) -> None:
        await self.connect()
        await self.subscribe(tickers)
        await self.poll_prices(interval)

    async def stop_streaming(self) -> None:
        await self.disconnect()
