"""
Portfolio optimization utilities — accelerated by Rust when available.
"""

from __future__ import annotations

import numpy as np

try:
    from miau_analytics._core import portfolio_stats as _rust_stats
    from miau_analytics._core import portfolio_evaluate as _rust_eval
    from miau_analytics._core import efficient_frontier as _rust_frontier

    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False


def portfolio_stats(prices: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute annualized mean returns and covariance matrix.

    Parameters
    ----------
    prices : ndarray, shape (days, tickers)

    Returns
    -------
    mean_returns : ndarray, shape (tickers,)
    cov_matrix : ndarray, shape (tickers, tickers)
    """
    if _HAS_RUST:
        import miau_analytics._core as _rust

        mu, cov = _rust.portfolio_stats(prices)
        return np.asarray(mu), np.asarray(cov)
    return _py_portfolio_stats(prices)


def portfolio_evaluate(
    weights: np.ndarray,
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.05,
) -> tuple[float, float, float]:
    """Evaluate a portfolio: (return, volatility, sharpe_ratio)."""
    if _HAS_RUST:
        import miau_analytics._core as _rust

        ret, vol, sharpe = _rust.portfolio_evaluate(weights, mean_returns, cov_matrix, risk_free_rate)
        return ret, vol, sharpe
    return _py_portfolio_evaluate(weights, mean_returns, cov_matrix, risk_free_rate)


def efficient_frontier(
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float = 0.05,
    num_points: int = 30,
) -> list[tuple[float, float, float]]:
    """Compute efficient frontier: list of (vol, ret, sharpe)."""
    if _HAS_RUST:
        import miau_analytics._core as _rust

        return list(_rust.efficient_frontier(mean_returns, cov_matrix, risk_free_rate, num_points))
    return _py_efficient_frontier(mean_returns, cov_matrix, risk_free_rate, num_points)


# ── Pure-Python fallbacks ────────────────────────────────────────────────────


def _py_portfolio_stats(prices: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    n_days, n_tickers = prices.shape
    if n_days < 2:
        return np.zeros(n_tickers), np.eye(n_tickers)

    returns = np.diff(np.log(prices), axis=0)
    mean_returns = np.mean(returns, axis=0) * 252
    cov_matrix = np.cov(returns, rowvar=False) * 252
    return mean_returns, cov_matrix


def _py_portfolio_evaluate(
    weights: np.ndarray,
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float,
) -> tuple[float, float, float]:
    port_ret = float(np.dot(weights, mean_returns))
    port_vol = float(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))
    sharpe = (port_ret - risk_free_rate) / port_vol if port_vol > 0 else 0.0
    return port_ret, port_vol, sharpe


def _py_efficient_frontier(
    mean_returns: np.ndarray,
    cov_matrix: np.ndarray,
    risk_free_rate: float,
    num_points: int,
) -> list[tuple[float, float, float]]:
    from scipy.optimize import minimize

    n = len(mean_returns)
    min_ret = float(mean_returns.min())
    max_ret = float(mean_returns.max())

    points = []
    for i in range(n):
        vol = float(np.sqrt(cov_matrix[i, i]))
        ret = float(mean_returns[i])
        sharpe = (ret - risk_free_rate) / vol if vol > 0 else 0
        points.append((vol, ret, sharpe))

    for k in range(num_points):
        target = min_ret + (max_ret - min_ret) * k / (num_points - 1)

        def neg_sharpe(w):
            ret = float(np.dot(w, mean_returns))
            vol = float(np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))))
            return -(ret - risk_free_rate) / vol if vol > 0 else 0

        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        bounds = [(0, 1)] * n
        guess = np.array([1 / n] * n)

        result = minimize(neg_sharpe, guess, method="SLSQP", bounds=bounds, constraints=constraints, options={"maxiter": 500})
        if result.success:
            w = result.x
            ret = float(np.dot(w, mean_returns))
            vol = float(np.sqrt(np.dot(w.T, np.dot(cov_matrix, w))))
            sharpe = (ret - risk_free_rate) / vol if vol > 0 else 0
            points.append((vol, ret, sharpe))

    points.sort(key=lambda x: x[0])
    return points[: num_points + n]
