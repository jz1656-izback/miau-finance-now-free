import logging
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime
from typing import Optional
from app.services.analytics._yf import get_history

logger = logging.getLogger(__name__)

try:
    from miau_analytics import (
        run_portfolio_stats as _rust_stats,
        portfolio_evaluate as _rust_eval,
        compute_efficient_frontier as _rust_frontier,
    )

    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False


async def _get_returns(tickers: list[str], period: str = "1y") -> pd.DataFrame:
    prices = {}
    for t in tickers:
        records = await get_history(t, period)
        if records:
            closes = [r["close"] for r in records if r.get("close")]
            if closes:
                prices[t] = closes
    if not prices:
        return pd.DataFrame()
    df = pd.DataFrame(prices)
    df = df.pct_change().dropna()
    return df


async def _get_prices_array(tickers: list[str], period: str = "1y") -> np.ndarray:
    """Get price matrix for Rust-accelerated stats."""
    prices = {}
    for t in tickers:
        records = await get_history(t, period)
        if records:
            closes = [r["close"] for r in records if r.get("close")]
            if closes:
                prices[t] = closes
    if not prices:
        return np.array([])
    df = pd.DataFrame(prices)
    return df.to_numpy(dtype=np.float64)


def _rust_portfolio_stats_impl(prices: np.ndarray, tickers: list[str]):
    """Compute mean returns + cov matrix via Rust, return pandas-compatible objects."""
    if _HAS_RUST and prices.size > 0:
        mu_arr, cov_arr = _rust_stats(prices)
        mean_ret = pd.Series(mu_arr, index=tickers)
        cov = pd.DataFrame(cov_arr, index=tickers, columns=tickers)
        return mean_ret, cov
    # Fallback: compute from log returns
    log_rets = np.diff(np.log(prices), axis=0)
    mean_ret = pd.Series(np.mean(log_rets, axis=0) * 252, index=tickers)
    cov = pd.DataFrame(np.cov(log_rets, rowvar=False) * 252, index=tickers, columns=tickers)
    return mean_ret, cov


async def optimize_portfolio(
    tickers: list[str],
    risk_free_rate: float = 0.05,
    target_return: Optional[float] = None,
    period: str = "1y",
) -> dict:
    returns = await _get_returns(tickers, period)
    if returns.empty or len(returns) < 10:
        return {"error": "Insufficient data for optimization"}

    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    n = len(tickers)

    def portfolio_stats(weights):
        ret = np.dot(weights, mean_returns)
        vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = (ret - risk_free_rate) / vol if vol > 0 else 0
        return ret, vol, sharpe

    def neg_sharpe(weights):
        return -portfolio_stats(weights)[2]

    constraints = [{"type": "eq", "fun": lambda x: np.sum(x) - 1}]
    bounds = tuple((0, 1) for _ in range(n))
    init_guess = np.array([1 / n] * n)

    opt = minimize(neg_sharpe, init_guess, method="SLSQP", bounds=bounds, constraints=constraints, options={"maxiter": 1000})
    if not opt.success:
        return {"error": "Optimization failed"}

    w = opt.x
    ret, vol, sharpe = portfolio_stats(w)

    result = {
        "tickers": tickers,
        "weights": {t: round(float(w[i]), 4) for i, t in enumerate(tickers)},
        "expected_return": round(float(ret), 4),
        "expected_volatility": round(float(vol), 4),
        "sharpe_ratio": round(float(sharpe), 4),
        "risk_free_rate": risk_free_rate,
    }

    # Efficient frontier (Rust-accelerated when available)
    frontier = []
    if _HAS_RUST:
        try:
            points = _rust_frontier(
                mean_returns.to_numpy(),
                cov_matrix.to_numpy(),
                risk_free_rate,
                30,
            )
            for vol, ret, _ in points:
                frontier.append({"return": round(float(ret), 4), "volatility": round(float(vol), 4)})
        except Exception as e:
            logger.warning(f"Efficient frontier computation failed: {e}")
            frontier = []
    if not frontier:
        target_rets = np.linspace(mean_returns.min(), mean_returns.max(), 15)
        for tr in target_rets:
            cons = [
                {"type": "eq", "fun": lambda x: np.sum(x) - 1},
                {"type": "eq", "fun": lambda x, tr=tr: np.dot(x, mean_returns) - tr},
            ]
            res = minimize(lambda w: np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))), init_guess, method="SLSQP", bounds=bounds, constraints=cons, options={"maxiter": 1000})
            if res.success:
                w2 = res.x
                frontier.append({"return": round(float(np.dot(w2, mean_returns)), 4), "volatility": round(float(np.sqrt(np.dot(w2.T, np.dot(cov_matrix, w2)))), 4)})
    result["efficient_frontier"] = frontier

    result["assets"] = [
        {"ticker": t, "expected_return": round(float(mean_returns.iloc[i]), 4), "volatility": round(float(np.sqrt(cov_matrix.iloc[i, i])), 4), "weight": round(float(w[i]), 4)}
        for i, t in enumerate(tickers)
    ]
    return result


async def min_variance_portfolio(tickers: list[str], period: str = "1y") -> dict:
    returns = await _get_returns(tickers, period)
    if returns.empty:
        return {"error": "No data"}
    cov_matrix = returns.cov() * 252
    n = len(tickers)

    def portfolio_vol(weights):
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

    constraints = [{"type": "eq", "fun": lambda x: np.sum(x) - 1}]
    bounds = tuple((0, 1) for _ in range(n))
    init_guess = np.array([1 / n] * n)
    opt = minimize(portfolio_vol, init_guess, method="SLSQP", bounds=bounds, constraints=constraints)
    if not opt.success:
        return {"error": "Optimization failed"}
    w = opt.x
    mean_returns = returns.mean() * 252
    return {
        "tickers": tickers,
        "weights": {t: round(float(w[i]), 4) for i, t in enumerate(tickers)},
        "expected_return": round(float(np.dot(w, mean_returns)), 4),
        "expected_volatility": round(float(portfolio_vol(w)), 4),
        "method": "min_variance",
    }


async def equal_weight_portfolio(tickers: list[str], period: str = "1y") -> dict:
    returns = await _get_returns(tickers, period)
    if returns.empty:
        return {"error": "No data"}
    n = len(tickers)
    w = np.array([1 / n] * n)
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    return {
        "tickers": tickers,
        "weights": {t: round(float(1 / n), 4) for t in tickers},
        "expected_return": round(float(np.dot(w, mean_returns)), 4),
        "expected_volatility": round(float(np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))), 4),
        "method": "equal_weight",
    }


def calculate_sharpe(returns: pd.Series, risk_free: float = 0.05) -> float:
    excess = returns - risk_free / 252
    return float(np.sqrt(252) * excess.mean() / excess.std()) if excess.std() > 0 else 0.0


def calculate_sortino(returns: pd.Series, risk_free: float = 0.05) -> float:
    excess = returns - risk_free / 252
    downside = excess[excess < 0].std()
    return float(np.sqrt(252) * excess.mean() / downside) if downside > 0 else 0.0


def calculate_max_drawdown(returns: pd.Series) -> dict:
    cum = (1 + returns).cumprod()
    running_max = cum.cummax()
    drawdown = (cum - running_max) / running_max
    return {"max_drawdown": float(drawdown.min()), "current_drawdown": float(drawdown.iloc[-1]) if not drawdown.empty else 0}
