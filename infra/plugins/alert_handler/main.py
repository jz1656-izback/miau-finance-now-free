"""Example plugin: custom alert handler that logs alerts to a file."""

import json
import logging
import os
from datetime import datetime
from typing import Any, Optional

from app.services.plugin.spec import HookPoint, PluginBase, PluginMeta

logger = logging.getLogger(__name__)

ALERT_LOG = os.environ.get("ALERT_PLUGIN_LOG", "/tmp/miau_alerts.jsonl")


class AlertHandlerPlugin(PluginBase):
    meta = PluginMeta(
        name="alert_handler",
        version="1.0.0",
        description="Logs market data anomalies to a JSONL file",
        author="Miau Finance",
        hooks=[HookPoint.AFTER_MARKET_DATA, HookPoint.ON_ERROR],
        permissions=["market:read"],
    )

    _alert_count: int = 0

    async def initialize(self) -> None:
        logger.info("AlertHandlerPlugin: initialized (log: %s)", ALERT_LOG)

    async def shutdown(self) -> None:
        logger.info("AlertHandlerPlugin: shutdown (%d alerts logged)", self._alert_count)

    async def after_market_data(self, data: dict[str, Any], **kw: Any) -> dict[str, Any]:
        anomalies = []
        for ticker, info in (data.get("data") or {}).items():
            if isinstance(info, dict):
                change = abs(float(info.get("change_pct", 0)))
                if change > 10:
                    anomalies.append({
                        "ticker": ticker,
                        "change_pct": change,
                        "price": info.get("price"),
                        "timestamp": datetime.utcnow().isoformat(),
                    })
        if anomalies:
            self._alert_count += len(anomalies)
            with open(ALERT_LOG, "a") as f:
                for alert in anomalies:
                    f.write(json.dumps(alert) + "\n")
            logger.info("AlertHandlerPlugin: logged %d anomalies", len(anomalies))
        return data

    async def on_error(self, error: Exception, context: dict[str, Any], **kw: Any) -> Optional[dict[str, Any]]:
        logger.warning("AlertHandlerPlugin: error context — %s", context)
        return None
