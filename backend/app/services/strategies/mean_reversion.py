import pandas as pd
from datetime import datetime
from app.services.strategies.base import StrategyBase, Signal
from app.services.strategies.registry import register


@register("mean_reversion")
class MeanReversionStrategy(StrategyBase):
    name = "mean_reversion"
    description = "Z-score mean reversion: BUY when price is far below its mean, SELL when far above"
    version = "1.0.0"

    def get_params(self) -> list[dict]:
        return [
            {"name": "lookback", "type": "int", "default": 20, "min": 5, "max": 100, "description": "Lookback period for mean"},
            {"name": "entry_z", "type": "float", "default": 2.0, "min": 0.5, "max": 5.0, "description": "Z-score entry threshold"},
            {"name": "exit_z", "type": "float", "default": 0.5, "min": 0.1, "max": 3.0, "description": "Z-score exit threshold"},
        ]

    def generate_signals(self, data: list[dict]) -> list[Signal]:
        signals = []
        if len(data) < self.get_params()[0]["default"]:
            return signals
        df = pd.DataFrame(data)
        close_col = "close" if "close" in df.columns else "Close"
        rolling_mean = df[close_col].rolling(self.get_params()[0]["default"]).mean()
        rolling_std = df[close_col].rolling(self.get_params()[0]["default"]).std()
        z_score = (df[close_col] - rolling_mean) / rolling_std
        in_position = False
        for i in range(1, len(df)):
            if pd.isna(z_score.iloc[i]):
                continue
            ts = df.index[i] if isinstance(df.index, pd.DatetimeIndex) else datetime.now()
            price = float(df[close_col].iloc[i])
            z = z_score.iloc[i]
            if not in_position and z < -self.get_params()[1]["default"]:
                signals.append(Signal(timestamp=ts, ticker="", action="BUY", strength=min(1.0, abs(z) / 3.0), price=price))
                in_position = True
            elif not in_position and z > self.get_params()[1]["default"]:
                signals.append(Signal(timestamp=ts, ticker="", action="SELL", strength=min(1.0, abs(z) / 3.0), price=price))
                in_position = True
            elif in_position and abs(z) < self.get_params()[2]["default"]:
                signals.append(Signal(timestamp=ts, ticker="", action="CLOSE", strength=0.5, price=price))
                in_position = False
        return signals
