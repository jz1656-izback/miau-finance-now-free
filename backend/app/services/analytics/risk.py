import numpy as np
import pandas as pd
from scipy import stats
from typing import Optional
from app.services.analytics._yf import get_history


async def _get_returns(ticker: str, period: str = "2y") -> pd.Series:
    records = await get_history(ticker, period)
    if not records:
        return pd.Series(dtype=float)
    closes = [r["close"] for r in records if r.get("close")]
    if len(closes) < 2:
        return pd.Series(dtype=float)
    s = pd.Series(closes).pct_change().dropna()
    return s


async def calculate_var(ticker: str, confidence: float = 0.95, method: str = "historical", period: str = "2y") -> dict:
    returns = await _get_returns(ticker, period)
    if returns.empty:
        return {"error": "Empty returns"}

    results = {"confidence": confidence, "method": method}
    if method == "historical":
        var = float(np.percentile(returns, (1 - confidence) * 100))
        cvar = float(returns[returns <= var].mean()) if len(returns[returns <= var]) > 0 else var
    elif method == "parametric":
        mu = returns.mean()
        sigma = returns.std()
        z = stats.norm.ppf(1 - confidence)
        var = float(mu + z * sigma)
        cvar = float(mu - sigma * stats.norm.pdf(z) / (1 - confidence))
    else:
        return {"error": f"Unknown method: {method}"}

    results["var"] = round(var, 6)
    results["cvar"] = round(cvar, 6)
    for label, days in [("1_day", 1), ("1_week", 5), ("2_weeks", 10), ("1_month", 21)]:
        results[f"var_{label}"] = round(var * np.sqrt(days), 6)
        results[f"cvar_{label}"] = round(cvar * np.sqrt(days), 6)
    return results


async def calculate_beta(ticker: str = "AAPL", benchmark: str = "SPY", period: str = "2y") -> dict:
    a = await _get_returns(ticker, period)
    b = await _get_returns(benchmark, period)
    if a.empty or b.empty:
        return {"error": "Insufficient data"}
    aligned = pd.concat([a, b], axis=1).dropna()
    if len(aligned) < 2:
        return {"error": "No aligned data"}
    cov = aligned.iloc[:, 0].cov(aligned.iloc[:, 1])
    var = aligned.iloc[:, 1].var()
    beta_val = cov / var if var != 0 else 1
    corr = aligned.iloc[:, 0].corr(aligned.iloc[:, 1])
    alpha = aligned.iloc[:, 0].mean() - beta_val * aligned.iloc[:, 1].mean()
    return {
        "beta": round(float(beta_val), 4),
        "alpha": round(float(alpha * 252), 6),
        "correlation": round(float(corr), 4),
        "r_squared": round(float(corr ** 2), 4),
    }


async def stress_test_scenarios(ticker: str = "SPY", period: str = "2y") -> dict:
    returns = await _get_returns(ticker, period)
    if returns.empty:
        return {"error": "Empty returns"}
    daily_vol = returns.std()
    scenarios = {
        "2008_financial_crisis": {"description": "-37% market crash (S&P 2008)", "shock": -0.37},
        "2020_covid": {"description": "-34% crash (Mar 2020)", "shock": -0.34},
        "2022_rate_hike": {"description": "-19% bear market (2022)", "shock": -0.19},
        "flash_crash": {"description": "-10% flash crash", "shock": -0.10},
        "correction": {"description": "-5% market correction", "shock": -0.05},
        "black_swan": {"description": "-50% extreme event", "shock": -0.50},
        "bull_run": {"description": "+20% bull market", "shock": 0.20},
    }
    results = {}
    for name, scenario in scenarios.items():
        prob = float(stats.norm.cdf(scenario["shock"] / daily_vol)) if daily_vol > 0 else 0.5
        results[name] = {
            "description": scenario["description"],
            "shock_pct": scenario["shock"],
            "approx_probability": round(prob, 4),
            "impact_label": f"{scenario['shock']*100:+.0f}%",
        }
    return results


async def comprehensive_risk(ticker: str = "AAPL", period: str = "2y") -> dict:
    a = await _get_returns(ticker, period)
    b = await _get_returns("SPY", period)
    if a.empty:
        return {"error": "No data"}

    var_95 = await calculate_var(ticker, 0.95, "historical", period)
    var_99 = await calculate_var(ticker, 0.99, "historical", period)
    stress = await stress_test_scenarios(ticker, period)
    beta_result = await calculate_beta(ticker, "SPY", period) if not b.empty else {}

    return {
        "ticker": ticker,
        "var_95": var_95,
        "var_99": var_99,
        "beta": beta_result,
        "stress_test": stress,
    }


def greeks_calc(spot: float, strike: float, time_to_expiry: float,
                risk_free: float, vol: float, option_type: str = "call") -> dict:
    from scipy.stats import norm
    if time_to_expiry <= 0 or vol <= 0 or spot <= 0:
        return {"error": "Invalid parameters"}
    d1 = (np.log(spot / strike) + (risk_free + 0.5 * vol ** 2) * time_to_expiry) / (vol * np.sqrt(time_to_expiry))
    d2 = d1 - vol * np.sqrt(time_to_expiry)
    is_call = option_type.lower() == "call"
    if is_call:
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (spot * vol * np.sqrt(time_to_expiry))
        theta = (-spot * norm.pdf(d1) * vol / (2 * np.sqrt(time_to_expiry)) - risk_free * strike * np.exp(-risk_free * time_to_expiry) * norm.cdf(d2)) / 365
        vega = spot * norm.pdf(d1) * np.sqrt(time_to_expiry) / 100
        rho = strike * time_to_expiry * np.exp(-risk_free * time_to_expiry) * norm.cdf(d2) / 100
        price = spot * norm.cdf(d1) - strike * np.exp(-risk_free * time_to_expiry) * norm.cdf(d2)
    else:
        delta = -norm.cdf(-d1)
        gamma = norm.pdf(d1) / (spot * vol * np.sqrt(time_to_expiry))
        theta = (-spot * norm.pdf(d1) * vol / (2 * np.sqrt(time_to_expiry)) + risk_free * strike * np.exp(-risk_free * time_to_expiry) * norm.cdf(-d2)) / 365
        vega = spot * norm.pdf(d1) * np.sqrt(time_to_expiry) / 100
        rho = -strike * time_to_expiry * np.exp(-risk_free * time_to_expiry) * norm.cdf(-d2) / 100
        price = strike * np.exp(-risk_free * time_to_expiry) * norm.cdf(-d2) - spot * norm.cdf(-d1)
    return {
        "option_type": option_type, "spot": round(spot, 2), "strike": round(strike, 2),
        "time_to_expiry": round(time_to_expiry, 4), "risk_free": risk_free,
        "volatility": vol, "price": round(float(price), 4),
        "delta": round(float(delta), 4), "gamma": round(float(gamma), 4),
        "theta": round(float(theta), 4), "vega": round(float(vega), 4), "rho": round(float(rho), 4),
    }


async def rolling_risk(
    ticker: str = "AAPL",
    benchmark: str = "SPY",
    window: str = "12mo",
    period: str = "3y",
) -> dict:
    import yfinance as yf
    import numpy as np
    from datetime import datetime

    t = yf.Ticker(ticker)
    b = yf.Ticker(benchmark)

    hist = t.history(period=period)
    bench_hist = b.history(period=period)

    if hist is None or bench_hist is None or hist.empty or bench_hist.empty:
        return {"error": f"No data for {ticker} or {benchmark}"}

    rets = hist["Close"].pct_change().dropna()
    bench_rets = bench_hist["Close"].pct_change().dropna()

    aligned = rets.to_frame("a").join(bench_rets.to_frame("b"), how="inner").dropna()
    if aligned.empty:
        return {"error": "No overlapping data"}

    day_map = {"3mo": 63, "6mo": 126, "12mo": 252, "24mo": 504}
    win = day_map.get(window, 252)

    rolling_sharpe = (aligned["a"].rolling(win).mean() / aligned["a"].rolling(win).std() * np.sqrt(252)).dropna()
    rolling_vol = (aligned["a"].rolling(win).std() * np.sqrt(252) * 100).dropna()
    covar = aligned["a"].rolling(win).cov(aligned["b"])
    bench_var = aligned["b"].rolling(win).var()
    rolling_beta = (covar / bench_var).dropna()

    return {
        "ticker": ticker.upper(),
        "benchmark": benchmark,
        "window": window,
        "period": period,
        "current_sharpe": round(float(rolling_sharpe.iloc[-1]) if len(rolling_sharpe) > 0 else 0, 2),
        "current_volatility_pct": round(float(rolling_vol.iloc[-1]) if len(rolling_vol) > 0 else 0, 1),
        "current_beta": round(float(rolling_beta.iloc[-1]) if len(rolling_beta) > 0 else 1, 2),
        "rolling_sharpe": {
            "dates": [str(d.date()) for d in rolling_sharpe.index[-20:]],
            "values": [round(float(v), 2) for v in rolling_sharpe.values[-20:]],
        },
        "rolling_beta": {
            "dates": [str(d.date()) for d in rolling_beta.index[-20:]],
            "values": [round(float(v), 2) for v in rolling_beta.values[-20:]],
        },
    }
