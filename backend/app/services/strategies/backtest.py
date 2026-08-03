from dataclasses import dataclass, field
from typing import Any
from app.services.strategies.registry import get_strategy, discover_strategies
from app.services.analytics._yf import get_history


@dataclass
class BacktestResult:
    strategy_name: str
    ticker: str
    initial_capital: float
    final_value: float
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    trades: list[dict] = field(default_factory=list)
    equity_curve: list[dict] = field(default_factory=list)


class BacktestEngine:
    def __init__(self, initial_capital: float = 100000.0, commission_pct: float = 0.001, slippage_pct: float = 0.0005):
        self.initial_capital = initial_capital
        self.commission_pct = commission_pct
        self.slippage_pct = slippage_pct

    async def run(self, strategy_name: str, ticker: str, period: str = "1y", params: dict | None = None) -> BacktestResult:
        discover_strategies()
        strategy_cls = get_strategy(strategy_name)
        strategy = strategy_cls()
        if params:
            for k, v in params.items():
                if hasattr(strategy, k):
                    setattr(strategy, k, v)

        range_map = {"1mo": "1mo", "3mo": "3mo", "6mo": "6mo", "1y": "1y", "2y": "2y"}
        records = await get_history(ticker, range_map.get(period, "1y"))
        if not records:
            return BacktestResult(strategy_name=strategy_name, ticker=ticker, initial_capital=self.initial_capital, final_value=self.initial_capital, total_return=0.0, sharpe_ratio=0.0, max_drawdown=0.0, win_rate=0.0, total_trades=0)

        signals = strategy.generate_signals(records)
        equity = self.initial_capital
        position = 0.0
        entry_price = 0.0
        trades = []
        equity_curve = []
        peak = self.initial_capital
        max_dd = 0.0
        wins = 0
        losses = 0
        daily_returns = []

        for i, row in enumerate(records):
            price = float(row.get("close", row.get("Close", 0)))
            timestamp = row.get("date", row.get("Date", ""))

            matching = [s for s in signals if str(s.timestamp) == str(timestamp)]
            for sig in matching:
                exec_price = price * (1 + self.slippage_pct) if sig.action == "BUY" else price * (1 - self.slippage_pct)
                commission = exec_price * (position if position > 0 else (equity / exec_price)) * self.commission_pct
                if sig.action == "BUY" and position == 0:
                    shares = (equity - commission) / exec_price
                    position = shares
                    equity = 0.0
                    entry_price = exec_price
                    trades.append({"type": "BUY", "price": round(exec_price, 4), "qty": round(shares, 4), "commission": round(commission, 2), "timestamp": str(timestamp)})
                elif sig.action == "SELL" and position > 0:
                    equity = position * exec_price - commission
                    pnl = position * (exec_price - entry_price)
                    trades.append({"type": "SELL", "price": round(exec_price, 4), "qty": round(position, 4), "pnl": round(pnl, 2), "commission": round(commission, 2), "timestamp": str(timestamp)})
                    if pnl > 0:
                        wins += 1
                    else:
                        losses += 1
                    position = 0.0

            portfolio_value = equity + position * price
            equity_curve.append({"timestamp": str(timestamp), "value": round(portfolio_value, 2)})
            if i > 0:
                prev_value = equity_curve[-2]["value"] if len(equity_curve) > 1 else self.initial_capital
                daily_returns.append((portfolio_value - prev_value) / prev_value if prev_value else 0)
            if portfolio_value > peak:
                peak = portfolio_value
            dd = (peak - portfolio_value) / peak * 100 if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd

        final_value = equity + position * (records[-1].get("close", records[-1].get("Close", 0)) if records else 0)
        total_return = (final_value - self.initial_capital) / self.initial_capital * 100 if self.initial_capital > 0 else 0

        n = len(daily_returns)
        avg_ret = sum(daily_returns) / n if n > 0 else 0
        std_ret = (sum((r - avg_ret) ** 2 for r in daily_returns) / n) ** 0.5 if n > 0 else 0
        sharpe = (avg_ret / std_ret * (252 ** 0.5)) if std_ret > 0 else 0
        win_rate = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0

        return BacktestResult(
            strategy_name=strategy_name,
            ticker=ticker,
            initial_capital=self.initial_capital,
            final_value=round(final_value, 2),
            total_return=round(total_return, 2),
            sharpe_ratio=round(sharpe, 4),
            max_drawdown=round(max_dd, 2),
            win_rate=round(win_rate, 2),
            total_trades=len(trades),
            trades=trades,
            equity_curve=equity_curve,
        )
