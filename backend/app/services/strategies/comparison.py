from dataclasses import dataclass, field
from typing import Any
from app.services.strategies.registry import discover_strategies, get_strategy


@dataclass
class StrategyRanking:
    rank: int
    strategy_name: str
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    score: float


@dataclass
class ComparisonResult:
    strategy_names: list[str] = field(default_factory=list)
    rankings: list[StrategyRanking] = field(default_factory=list)
    correlation_matrix: list[list[float]] = field(default_factory=list)
    best_strategy: str = ""
    worst_strategy: str = ""


class StrategyComparer:
    def __init__(self, strategies: list[str]):
        self.strategies = strategies
        discover_strategies()

    async def compare(self, ticker: str, period: str = "1y") -> ComparisonResult:
        from app.services.analytics._yf import get_history

        range_map = {"1mo": "1mo", "3mo": "3mo", "6mo": "6mo", "1y": "1y", "2y": "2y"}
        records = await get_history(ticker, range_map.get(period, "1y"))
        if not records:
            return ComparisonResult(strategy_names=self.strategies)

        rankings = []
        daily_returns_map: dict[str, list[float]] = {}

        for sname in self.strategies:
            try:
                strategy_cls = get_strategy(sname)
                if strategy_cls is None:
                    continue
                strategy = strategy_cls()
                result = strategy.backtest(records)
                trades = result.get("trades", [])
                equity_curve = result.get("equity_curve", [])

                total_return = result.get("total_return", 0)
                total_trades = result.get("total_trades", 0)

                daily_returns = []
                peak = 100000.0
                max_dd = 0.0
                for i, point in enumerate(equity_curve):
                    val = point.get("value", 100000.0)
                    if val > peak:
                        peak = val
                    dd = (peak - val) / peak * 100 if peak > 0 else 0
                    if dd > max_dd:
                        max_dd = dd
                    if i > 0:
                        prev = equity_curve[i - 1].get("value", 100000.0)
                        daily_returns.append((val - prev) / prev if prev > 0 else 0)

                n = len(daily_returns)
                avg_ret = sum(daily_returns) / n if n > 0 else 0
                std_ret = (sum((r - avg_ret) ** 2 for r in daily_returns) / n) ** 0.5 if n > 0 else 0
                sharpe = (avg_ret / std_ret * (252 ** 0.5)) if std_ret > 0 else 0

                wins = sum(1 for t in trades if t.get("type") == "SELL" and t.get("pnl", 0) > 0)
                losses = sum(1 for t in trades if t.get("type") == "SELL" and t.get("pnl", 0) <= 0)
                win_rate = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0

                norm_return = (total_return + 100) / 200 if -100 < total_return < 100 else 0.5
                norm_sharpe = min(1.0, max(0.0, sharpe / 3.0))
                norm_dd = max(0.0, 1.0 - max_dd / 50.0)
                norm_wr = win_rate / 100.0
                score = norm_return * 0.3 + norm_sharpe * 0.3 + norm_dd * 0.2 + norm_wr * 0.2

                rankings.append(StrategyRanking(
                    rank=0,
                    strategy_name=sname,
                    total_return=round(total_return, 2),
                    sharpe_ratio=round(sharpe, 4),
                    max_drawdown=round(max_dd, 2),
                    win_rate=round(win_rate, 2),
                    total_trades=total_trades,
                    score=round(score, 4),
                ))
                daily_returns_map[sname] = daily_returns
            except Exception:
                continue

        rankings.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(rankings):
            r.rank = i + 1

        names = [r.strategy_name for r in rankings]
        corr_matrix = []
        for s1 in names:
            row = []
            r1 = daily_returns_map.get(s1, [])
            for s2 in names:
                r2 = daily_returns_map.get(s2, [])
                if len(r1) < 2 or len(r2) < 2:
                    row.append(0.0)
                    continue
                min_len = min(len(r1), len(r2))
                a = r1[:min_len]
                b = r2[:min_len]
                mean_a = sum(a) / len(a)
                mean_b = sum(b) / len(b)
                num = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b))
                den_a = sum((x - mean_a) ** 2 for x in a) ** 0.5
                den_b = sum((y - mean_b) ** 2 for y in b) ** 0.5
                corr = num / (den_a * den_b) if den_a > 0 and den_b > 0 else 0.0
                row.append(round(corr, 4))
            corr_matrix.append(row)

        best = rankings[0].strategy_name if rankings else ""
        worst = rankings[-1].strategy_name if rankings else ""

        return ComparisonResult(
            strategy_names=names,
            rankings=rankings,
            correlation_matrix=corr_matrix,
            best_strategy=best,
            worst_strategy=worst,
        )
