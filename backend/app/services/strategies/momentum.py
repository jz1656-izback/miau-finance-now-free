import pandas as pd
from datetime import datetime
from app.services.strategies.base import StrategyBase, Signal
from app.services.strategies.registry import register


@register("momentum")
class MomentumStrategy(StrategyBase):
    name = "momentum"
    description = "Momentum: BUY when price exceeds return threshold, SELL when it drops below"
    version = "1.0.0"

    def get_params(self) -> list[dict]:
        return [
            {"name": "lookback", "type": "int", "default": 20, "min": 5, "max": 100, "description": "Return calculation period"},
            {"name": "entry_threshold", "type": "float", "default": 0.05, "min": 0.01, "max": 0.5, "description": "Entry return threshold"},
            {"name": "exit_threshold", "type": "float", "default": 0.02, "min": 0.0, "max": 0.3, "description": "Exit return threshold"},
        ]

    def generate_signals(self, data: list[dict]) -> list[Signal]:
        signals = []
        if len(data) < self.get_params()[0]["default"] + 1:
            return signals
        df = pd.DataFrame(data)
        close_col = "close" if "close" in df.columns else "Close"
        returns = df[close_col].pct_change(self.get_params()[0]["default"])
        in_position = False
        for i in range(1, len(df)):
            if pd.isna(returns.iloc[i]):
                continue
            ts = df.index[i] if isinstance(df.index, pd.DatetimeIndex) else datetime.now()
            price = float(df[close_col].iloc[i])
            ret = returns.iloc[i]
            if not in_position and ret > self.get_params()[1]["default"]:
                signals.append(Signal(timestamp=ts, ticker="", action="BUY", strength=min(1.0, ret / 0.1), price=price))
                in_position = True
            elif in_position and ret < self.get_params()[2]["default"]:
                signals.append(Signal(timestamp=ts, ticker="", action="SELL", strength=0.5, price=price))
                in_position = False
        return signals
