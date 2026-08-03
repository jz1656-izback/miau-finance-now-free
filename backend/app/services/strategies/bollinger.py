import pandas as pd
from datetime import datetime
from app.services.strategies.base import StrategyBase, Signal
from app.services.strategies.registry import register


@register("bollinger")
class BollingerStrategy(StrategyBase):
    name = "bollinger"
    description = "Bollinger Bands mean reversion: BUY at lower band, SELL at upper band"
    version = "1.0.0"

    def get_params(self) -> list[dict]:
        return [
            {"name": "period", "type": "int", "default": 20, "min": 5, "max": 100, "description": "Rolling window period"},
            {"name": "std_dev", "type": "float", "default": 2.0, "min": 1.0, "max": 5.0, "description": "Standard deviation multiplier"},
        ]

    def generate_signals(self, data: list[dict]) -> list[Signal]:
        signals = []
        if len(data) < self.get_params()[0]["default"]:
            return signals
        df = pd.DataFrame(data)
        close_col = "close" if "close" in df.columns else "Close"
        sma = df[close_col].rolling(self.get_params()[0]["default"]).mean()
        std = df[close_col].rolling(self.get_params()[0]["default"]).std()
        upper = sma + self.get_params()[1]["default"] * std
        lower = sma - self.get_params()[1]["default"] * std
        for i in range(1, len(df)):
            if pd.isna(upper.iloc[i]) or pd.isna(lower.iloc[i]):
                continue
            ts = df.index[i] if isinstance(df.index, pd.DatetimeIndex) else datetime.now()
            price = float(df[close_col].iloc[i])
            if price <= lower.iloc[i]:
                signals.append(Signal(timestamp=ts, ticker="", action="BUY", strength=1.0, price=price))
            elif price >= upper.iloc[i]:
                signals.append(Signal(timestamp=ts, ticker="", action="SELL", strength=1.0, price=price))
        return signals
