import pandas as pd
from datetime import datetime
from app.services.strategies.base import StrategyBase, Signal
from app.services.strategies.registry import register


@register("rsi")
class RSIStrategy(StrategyBase):
    name = "rsi"
    description = "RSI mean reversion: BUY when oversold (<30), SELL when overbought (>70)"
    version = "1.0.0"

    def get_params(self) -> list[dict]:
        return [
            {"name": "rsi_period", "type": "int", "default": 14, "min": 2, "max": 100, "description": "RSI calculation period"},
            {"name": "overbought", "type": "int", "default": 70, "min": 50, "max": 100, "description": "Overbought threshold"},
            {"name": "oversold", "type": "int", "default": 30, "min": 0, "max": 50, "description": "Oversold threshold"},
        ]

    def generate_signals(self, data: list[dict]) -> list[Signal]:
        signals = []
        if len(data) < self.get_params()[0]["default"] + 1:
            return signals
        df = pd.DataFrame(data)
        close_col = "close" if "close" in df.columns else "Close"
        delta = df[close_col].diff()
        gain = delta.where(delta > 0, 0).rolling(self.get_params()[0]["default"]).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.get_params()[0]["default"]).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        for i in range(1, len(df)):
            if pd.isna(rsi.iloc[i]):
                continue
            ts = df.index[i] if isinstance(df.index, pd.DatetimeIndex) else datetime.now()
            if rsi.iloc[i] < self.get_params()[2]["default"]:
                signals.append(Signal(timestamp=ts, ticker="", action="BUY", strength=1.0, price=float(df[close_col].iloc[i])))
            elif rsi.iloc[i] > self.get_params()[1]["default"]:
                signals.append(Signal(timestamp=ts, ticker="", action="SELL", strength=1.0, price=float(df[close_col].iloc[i])))
        return signals
