from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime


@dataclass
class Signal:
    timestamp: datetime
    ticker: str
    action: str
    strength: float
    price: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StrategyInfo:
    name: str
    description: str
    version: str
    params: list[dict[str, Any]]


class StrategyBase(ABC):
    name: str = ""
    description: str = ""
    version: str = "1.0.0"

    @abstractmethod
    def get_params(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def generate_signals(self, data: list[dict[str, Any]]) -> list[Signal]:
        ...

    def backtest(self, data: list[dict[str, Any]]) -> dict[str, Any]:
        signals = self.generate_signals(data)
        equity = 100000.0
        position = 0.0
        entry_price = 0.0
        trades = []
        equity_curve = []

        for i, row in enumerate(data):
            price = float(row.get("close", row.get("Close", 0)))
            timestamp = row.get("date", row.get("Date", ""))
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp)
                except ValueError:
                    timestamp = datetime.now()

            matching = [s for s in signals if s.timestamp == timestamp]
            for sig in matching:
                if sig.action == "BUY" and position == 0:
                    position = equity / price
                    entry_price = price
                    equity = 0.0
                    trades.append({"type": "BUY", "price": price, "timestamp": str(timestamp)})
                elif sig.action == "SELL" and position > 0:
                    equity = position * price
                    trades.append({"type": "SELL", "price": price, "pnl": position * (price - entry_price), "timestamp": str(timestamp)})
                    position = 0.0

            portfolio_value = equity + position * price
            equity_curve.append({"timestamp": str(timestamp), "value": round(portfolio_value, 2)})

        final_value = equity + position * (data[-1]["close"] if data else 0)
        returns = (final_value - 100000.0) / 100000.0 if data else 0.0

        return {
            "strategy": self.name,
            "initial_capital": 100000.0,
            "final_value": round(final_value, 2),
            "total_return": round(returns * 100, 2),
            "total_trades": len(trades),
            "trades": trades,
            "equity_curve": equity_curve,
        }

    def get_info(self) -> StrategyInfo:
        return StrategyInfo(
            name=self.name,
            description=self.description,
            version=self.version,
            params=self.get_params(),
        )
