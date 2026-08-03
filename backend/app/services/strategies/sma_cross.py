import pandas as pd
from datetime import datetime
from app.services.strategies.base import StrategyBase, Signal
from app.services.strategies.registry import register


@register("sma_cross")
class SMACrossStrategy(StrategyBase):
    name = "sma_cross"
    description = "SMA crossover: BUY when fast SMA crosses above slow SMA, SELL when it crosses below"
    version = "1.0.0"

    def get_params(self) -> list[dict]:
        return [
            {"name": "fast_period", "type": "int", "default": 10, "min": 2, "max": 100, "description": "Fast SMA period"},
            {"name": "slow_period", "type": "int", "default": 50, "min": 5, "max": 500, "description": "Slow SMA period"},
        ]

    def generate_signals(self, data: list[dict]) -> list[Signal]:
        signals = []
        if len(data) < self.get_params()[1]["default"]:
            return signals
        df = pd.DataFrame(data)
        close_col = "close" if "close" in df.columns else "Close"
        df["fast_sma"] = df[close_col].rolling(self.get_params()[0]["default"]).mean()
        df["slow_sma"] = df[close_col].rolling(self.get_params()[1]["default"]).mean()
        for i in range(1, len(df)):
            if pd.isna(df["fast_sma"].iloc[i]) or pd.isna(df["slow_sma"].iloc[i]):
                continue
            prev_fast = df["fast_sma"].iloc[i - 1]
            prev_slow = df["slow_sma"].iloc[i - 1]
            curr_fast = df["fast_sma"].iloc[i]
            curr_slow = df["slow_sma"].iloc[i]
            ts = df.index[i] if isinstance(df.index, pd.DatetimeIndex) else datetime.now()
            if prev_fast <= prev_slow and curr_fast > curr_slow:
                signals.append(Signal(timestamp=ts, ticker="", action="BUY", strength=1.0, price=float(df[close_col].iloc[i])))
            elif prev_fast >= prev_slow and curr_fast < curr_slow:
                signals.append(Signal(timestamp=ts, ticker="", action="SELL", strength=1.0, price=float(df[close_col].iloc[i])))
        return signals
