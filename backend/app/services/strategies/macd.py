import pandas as pd
from datetime import datetime
from app.services.strategies.base import StrategyBase, Signal
from app.services.strategies.registry import register


@register("macd")
class MACDStrategy(StrategyBase):
    name = "macd"
    description = "MACD crossover: BUY when MACD crosses above signal line, SELL when it crosses below"
    version = "1.0.0"

    def get_params(self) -> list[dict]:
        return [
            {"name": "fast_period", "type": "int", "default": 12, "min": 2, "max": 100, "description": "Fast EMA period"},
            {"name": "slow_period", "type": "int", "default": 26, "min": 5, "max": 200, "description": "Slow EMA period"},
            {"name": "signal_period", "type": "int", "default": 9, "min": 2, "max": 50, "description": "Signal line period"},
        ]

    def generate_signals(self, data: list[dict]) -> list[Signal]:
        signals = []
        if len(data) < self.get_params()[1]["default"] + 1:
            return signals
        df = pd.DataFrame(data)
        close_col = "close" if "close" in df.columns else "Close"
        ema_fast = df[close_col].ewm(span=self.get_params()[0]["default"]).mean()
        ema_slow = df[close_col].ewm(span=self.get_params()[1]["default"]).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=self.get_params()[2]["default"]).mean()
        for i in range(1, len(df)):
            if pd.isna(macd.iloc[i]) or pd.isna(signal.iloc[i]):
                continue
            ts = df.index[i] if isinstance(df.index, pd.DatetimeIndex) else datetime.now()
            if macd.iloc[i - 1] <= signal.iloc[i - 1] and macd.iloc[i] > signal.iloc[i]:
                signals.append(Signal(timestamp=ts, ticker="", action="BUY", strength=1.0, price=float(df[close_col].iloc[i])))
            elif macd.iloc[i - 1] >= signal.iloc[i - 1] and macd.iloc[i] < signal.iloc[i]:
                signals.append(Signal(timestamp=ts, ticker="", action="SELL", strength=1.0, price=float(df[close_col].iloc[i])))
        return signals
