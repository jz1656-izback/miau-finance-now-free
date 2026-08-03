"""Example plugin: custom trading strategy that logs signals to a file."""

import json
import logging
import os
from datetime import datetime
from typing import Any, Optional

from app.services.plugin.spec import HookPoint, PluginBase, PluginMeta

logger = logging.getLogger(__name__)

SIGNAL_LOG = os.environ.get("STRATEGY_PLUGIN_LOG", "/tmp/miau_strategy_signals.jsonl")


class CustomStrategyPlugin(PluginBase):
    meta = PluginMeta(
        name="custom_strategy",
        version="1.0.0",
        description="Generates custom trading signals based on market data patterns",
        author="Miau Finance",
        hooks=[HookPoint.ON_ANALYTICS, HookPoint.BEFORE_ORDER],
        permissions=["market:read", "orders:create"],
    )

    _signal_count: int = 0

    async def initialize(self) -> None:
        logger.info("CustomStrategyPlugin: initialized (signal log: %s)", SIGNAL_LOG)

    async def shutdown(self) -> None:
        logger.info("CustomStrategyPlugin: shutdown (%d signals generated)", self._signal_count)

    async def on_analytics(self, ticker: str, analytics: dict[str, Any], **kw: Any) -> dict[str, Any]:
        price = analytics.get("current_price", 0)
        rsi = analytics.get("rsi", 50)
        sma_short = analytics.get("sma_20", 0)
        sma_long = analytics.get("sma_50", 0)
        volume = analytics.get("volume", 0)
        avg_volume = analytics.get("avg_volume", 1)

        signals = []

        if rsi < 30 and volume > avg_volume * 1.5:
            signals.append({"type": "BUY", "reason": f"Oversold (RSI={rsi:.1f}) with high volume", "confidence": "high"})
        elif rsi > 70 and volume > avg_volume * 1.5:
            signals.append({"type": "SELL", "reason": f"Overbought (RSI={rsi:.1f}) with high volume", "confidence": "high"})

        if sma_short and sma_long and sma_short > sma_long:
            signals.append({"type": "BUY", "reason": f"Golden cross SMA20 ({sma_short:.2f}) > SMA50 ({sma_long:.2f})", "confidence": "medium"})
        elif sma_short and sma_long and sma_short < sma_long:
            signals.append({"type": "SELL", "reason": f"Death cross SMA20 ({sma_short:.2f}) < SMA50 ({sma_long:.2f})", "confidence": "medium"})

        if signals:
            self._signal_count += len(signals)
            entry = {"ticker": ticker, "price": price, "signals": signals, "timestamp": datetime.utcnow().isoformat()}
            with open(SIGNAL_LOG, "a") as f:
                f.write(json.dumps(entry) + "\n")

        analytics["custom_strategy_signals"] = signals
        return analytics

    async def before_order(self, order: dict[str, Any], **kw: Any) -> dict[str, Any]:
        symbol = order.get("symbol", "")
        qty = order.get("qty", 0)
        side = order.get("side", "BUY")

        if qty > 10000:
            order["max_show"] = 1000
            order["iceberg"] = True
            logger.info("CustomStrategyPlugin: iceberg order for %s %s %d", side, symbol, qty)

        return order
