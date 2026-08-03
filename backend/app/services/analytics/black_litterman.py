import numpy as np
import pandas as pd
from datetime import datetime
from app.services.analytics._yf import get_history
from app.services.analytics.portfolio_optimizer import calculate_sharpe


def _black_litterman_python(
    prior_returns: np.ndarray,
    cov_matrix: np.ndarray,
    view_matrix: np.ndarray,
    view_returns: np.ndarray,
    view_uncertainty: np.ndarray,
    tau: float,
) -> np.ndarray:
    omega = np.diag(view_uncertainty)
    inv_tau_sigma = np.linalg.inv(tau * cov_matrix)
    inv_omega = np.linalg.inv(omega)
    M = inv_tau_sigma + view_matrix.T @ inv_omega @ view_matrix
    posterior = np.linalg.inv(M) @ (inv_tau_sigma @ prior_returns + view_matrix.T @ inv_omega @ view_returns)
    return posterior


def _black_litterman_posterior(
    prior_returns: np.ndarray,
    cov_matrix: np.ndarray,
    view_matrix: np.ndarray,
    view_returns: np.ndarray,
    view_uncertainty: np.ndarray,
    tau: float = 0.05,
) -> np.ndarray:
    try:
        from miau_analytics._core import black_litterman_implied_returns, black_litterman_posterior
        return np.asarray(black_litterman_posterior(
            prior_returns, cov_matrix, tau,
            view_matrix, view_returns, view_uncertainty,
        ))
    except (ImportError, Exception) as e:
        import logging
        logging.getLogger(__name__).debug("Rust BL fallback: %s", e)
        return _black_litterman_python(prior_returns, cov_matrix, view_matrix, view_returns, view_uncertainty, tau)


async def black_litterman(
    tickers: list[str],
    market_cap_weights: list[float],
    views: list[dict],
    risk_aversion: float = 2.5,
    period: str = "2y",
) -> dict:
    if len(tickers) != len(market_cap_weights):
        return {"error": "tickers and market_cap_weights must have same length"}

    n = len(tickers)
    market_weights = np.array(market_cap_weights, dtype=float)
    market_weights = market_weights / market_weights.sum()

    prices = {}
    for t in tickers:
        records = await get_history(t, period)
        if not records:
            return {"error": f"No data for {t}"}
        closes = [r["close"] for r in records if r.get("close")]
        if len(closes) < 20:
            return {"error": f"Insufficient data for {t}"}
        prices[t] = closes

    df = pd.DataFrame(prices)
    returns = df.pct_change().dropna()
    if returns.empty or len(returns) < 10:
        return {"error": "Insufficient return data"}

    mean_returns = returns.mean().values * 252
    cov_matrix = returns.cov().values * 252

    delta = risk_aversion
    pi = delta * cov_matrix @ market_weights

    k = len(views)
    if k == 0:
        posterior_returns = pi
        posterior_cov = cov_matrix
        weights = market_weights
    else:
        P = np.zeros((k, n))
        Q = np.zeros(k)
        omega = np.zeros((k, k))

        for i, v in enumerate(views):
            ticker = v.get("ticker")
            if ticker not in tickers:
                return {"error": f"View ticker {ticker} not in universe"}
            idx = tickers.index(ticker)
            view_type = v.get("view_type", "absolute")
            q = v.get("q", 0)
            confidence = v.get("confidence", 0.5)

            if view_type == "absolute":
                P[i, idx] = 1
                Q[i] = q
            elif view_type == "relative_outperform":
                other = v.get("relative_ticker")
                if other not in tickers:
                    return {"error": f"Relative ticker {other} not in universe"}
                oidx = tickers.index(other)
                P[i, idx] = 1
                P[i, oidx] = -1
                Q[i] = q
            else:
                return {"error": f"Unknown view_type: {view_type}"}

            tau = 0.05
            omega[i, i] = (1 - confidence) / confidence * (P[i, :] @ cov_matrix @ P[i, :]) * tau

        tau = 0.05
        posterior_returns = _black_litterman_posterior(
            pi, cov_matrix, P, Q, np.diag(omega) if omega.ndim > 1 else omega, tau
        )
        posterior_cov = cov_matrix + np.linalg.inv(
            np.linalg.inv(tau * cov_matrix) + P.T @ np.linalg.inv(omega) @ P
        )

        weights = np.linalg.solve(delta * posterior_cov, posterior_returns)
        weights = np.maximum(weights, 0)
        weights = weights / weights.sum() if weights.sum() > 0 else market_weights

    port_ret = float(np.dot(weights, posterior_returns))
    port_vol = float(np.sqrt(np.dot(weights.T, np.dot(posterior_cov, weights))))
    sharpe = (port_ret - 0.05) / port_vol if port_vol > 0 else 0

    return {
        "tickers": tickers,
        "weights": {t: round(float(w), 4) for t, w in zip(tickers, weights)},
        "implied_returns": {t: round(float(pi[i]), 6) for i, t in enumerate(tickers)},
        "posterior_returns": {t: round(float(posterior_returns[i]), 6) for i, t in enumerate(tickers)},
        "portfolio": {
            "expected_return": round(port_ret, 4),
            "expected_volatility": round(port_vol, 4),
            "sharpe_ratio": round(sharpe, 4),
        },
        "risk_aversion": risk_aversion,
        "num_views": k,
        "as_of": datetime.now().isoformat(),
    }
