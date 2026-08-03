"""Econometrics & Quant engine — OLS, Granger, Cointegration, CAPM, Correlation."""
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from typing import Optional
from app.services.analytics._yf import get_history
from app.services.data.providers.yahoo import YahooProvider


def _hist_to_df(records: list) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["date"])
    df.set_index("Date", inplace=True)
    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"}, inplace=True)
    return df


async def _get_returns(ticker: str, period: str = "1y") -> pd.Series:
    records = await get_history(ticker, period)
    if not records:
        return pd.Series(dtype=float)
    closes = [r["close"] for r in records if r.get("close")]
    if len(closes) < 10:
        return pd.Series(dtype=float)
    return pd.Series(closes).pct_change().dropna()


async def _get_prices(ticker: str, period: str = "1y") -> pd.Series:
    records = await get_history(ticker, period)
    if not records:
        return pd.Series(dtype=float)
    closes = [r["close"] for r in records if r.get("close")]
    if len(closes) < 10:
        return pd.Series(dtype=float)
    return pd.Series(closes, index=pd.date_range(end=pd.Timestamp.now(), periods=len(closes), freq="D"))


async def ols_regression(y_ticker: str, x_ticker: str, period: str = "1y") -> dict:
    y_prices = await _get_prices(y_ticker, period)
    x_prices = await _get_prices(x_ticker, period)
    if len(y_prices) < 10 or len(x_prices) < 10:
        return {"error": "Insufficient data"}
    # Align
    common = pd.concat([y_prices, x_prices], axis=1).dropna()
    if len(common) < 10:
        return {"error": "Insufficient overlapping data"}
    y = common.iloc[:, 0].values
    x = common.iloc[:, 1].values
    X = add_constant(x)
    model = OLS(y, X).fit()
    return {
        "dependent": y_ticker,
        "independent": x_ticker,
        "observations": len(common),
        "r_squared": round(model.rsquared, 4),
        "adj_r_squared": round(model.rsquared_adj, 4),
        "coefficient": round(model.params[1], 6),
        "intercept": round(model.params[0], 6),
        "p_value": round(model.pvalues[1], 6),
        "t_statistic": round(model.tvalues[1], 4),
        "std_err": round(model.bse[1], 6),
        "f_statistic": round(model.fvalue, 2),
        "f_p_value": round(model.f_pvalue, 6),
        "equation": f"{y_ticker} = {model.params[0]:.4f} + {model.params[1]:.4f} × {x_ticker}",
        "cat_commentary": "The cat fitted a line through the data. The line purrs.",
    }


async def granger_causality(y_ticker: str, x_ticker: str, max_lag: int = 5, period: str = "1y") -> dict:
    y_prices = await _get_prices(y_ticker, period)
    x_prices = await _get_prices(x_ticker, period)
    common = pd.concat([y_prices, x_prices], axis=1).dropna()
    if len(common) < 20:
        return {"error": "Insufficient data (need 20+ observations)"}
    data = common.values
    try:
        test_result = grangercausalitytests(data, maxlag=min(max_lag, len(data) // 3), verbose=False)
    except Exception as e:
        return {"error": f"Granger test failed: {e}"}
    results = []
    for lag, result in test_result.items():
        f_test = result[0]["ssr_ftest"]
        results.append({
            "lag": lag,
            "f_statistic": round(float(f_test[0]), 4),
            "p_value": round(float(f_test[1]), 6),
            "significant": bool(f_test[1] < 0.05),
        })
    significant_lags = [r for r in results if r["significant"]]
    return {
        "y": y_ticker,
        "x": x_ticker,
        "results": results,
        "significant_at": [r["lag"] for r in significant_lags],
        "conclusion": f"{'✅' if significant_lags else '❌'} {x_ticker}"
            + (f" Granger-causes {y_ticker} at lags {[r['lag'] for r in significant_lags]}"
               if significant_lags else f" does NOT Granger-cause {y_ticker}"),
        "cat_commentary": "The cat conducted a causality test. The p-value purrs.",
    }


async def cointegration_test(y_ticker: str, x_ticker: str, period: str = "2y") -> dict:
    y_prices = await _get_prices(y_ticker, period)
    x_prices = await _get_prices(x_ticker, period)
    common = pd.concat([y_prices, x_prices], axis=1).dropna()
    if len(common) < 30:
        return {"error": "Insufficient data"}
    y = common.iloc[:, 0].values
    x = common.iloc[:, 1].values
    X = add_constant(x)
    model = OLS(y, X).fit()
    residuals = model.resid
    adf_result = adfuller(residuals, autolag="AIC")
    adf_stat = float(adf_result[0])
    adf_pvalue = float(adf_result[1])
    critical_values = {k: float(v) for k, v in adf_result[4].items()}
    is_cointegrated = adf_pvalue < 0.05
    hedge_ratio = float(model.params[1])
    spread = y - hedge_ratio * x
    return {
        "pair": f"{y_ticker} / {x_ticker}",
        "hedge_ratio": round(hedge_ratio, 4),
        "adf_statistic": round(adf_stat, 4),
        "adf_p_value": round(adf_pvalue, 6),
        "critical_values": critical_values,
        "is_cointegrated": is_cointegrated,
        "current_spread": round(float(spread[-1]), 4),
        "spread_mean": round(float(np.mean(spread)), 4),
        "spread_std": round(float(np.std(spread)), 4),
        "z_score": round(float((spread[-1] - np.mean(spread)) / np.std(spread)), 4) if np.std(spread) > 0 else 0,
        "conclusion": "✅ Cointegrated — these two move together like cat and nap"
            if is_cointegrated else "❌ Not cointegrated — they're like cat and bathwater",
        "cat_commentary": "The cat checked if these two are secretly related. They might be siblings.",
    }


async def capm_analysis(ticker: str, benchmark: str = "SPY", period: str = "2y", risk_free_rate: float = 0.05) -> dict:
    asset_returns = await _get_returns(ticker, period)
    bench_returns = await _get_returns(benchmark, period)
    common = pd.concat([asset_returns, bench_returns], axis=1).dropna()
    if len(common) < 20:
        return {"error": "Insufficient data"}
    asset_r = common.iloc[:, 0].values
    bench_r = common.iloc[:, 1].values
    excess_asset = asset_r - risk_free_rate / 252
    excess_bench = bench_r - risk_free_rate / 252
    X = add_constant(excess_bench)
    model = OLS(excess_asset, X).fit()
    alpha = float(model.params[0]) * 252  # annualize
    beta = float(model.params[1])
    # Metrics
    annual_asset_return = float(np.mean(asset_r)) * 252
    annual_bench_return = float(np.mean(bench_r)) * 252
    asset_vol = float(np.std(asset_r)) * np.sqrt(252)
    bench_vol = float(np.std(bench_r)) * np.sqrt(252)
    sharpe = (annual_asset_return - risk_free_rate) / asset_vol if asset_vol > 0 else 0
    treynor = (annual_asset_return - risk_free_rate) / beta if beta != 0 else 0
    tracking_error = float(np.std(asset_r - bench_r)) * np.sqrt(252)
    info_ratio = (annual_asset_return - annual_bench_return) / tracking_error if tracking_error > 0 else 0
    r_squared = float(model.rsquared)
    return {
        "ticker": ticker,
        "benchmark": benchmark,
        "alpha": round(alpha * 100, 2),
        "beta": round(beta, 4),
        "r_squared": round(r_squared, 4),
        "sharpe_ratio": round(sharpe, 4),
        "treynor_ratio": round(treynor, 4),
        "info_ratio": round(info_ratio, 4),
        "annual_return": round(annual_asset_return * 100, 2),
        "annual_volatility": round(asset_vol * 100, 2),
        "benchmark_return": round(annual_bench_return * 100, 2),
        "benchmark_volatility": round(bench_vol * 100, 2),
        "tracking_error": round(tracking_error * 100, 2),
        "risk_free_rate": risk_free_rate,
        "cat_commentary": f"The cat assessed the risk. Beta is {beta:.2f}. The cat is {'🐱 calm' if beta < 1 else '😼 aggressive' if beta > 1.3 else '😺 moderate'}.",
    }


async def correlation_matrix(tickers: list[str], period: str = "1y") -> dict:
    if len(tickers) < 2:
        return {"error": "Need at least 2 tickers"}
    returns_dict = {}
    for ticker in tickers:
        try:
            r = await _get_returns(ticker, period)
            if not r.empty:
                returns_dict[ticker] = r
        except Exception:
            continue
    if len(returns_dict) < 2:
        return {"error": "Insufficient data for correlation"}
    df = pd.DataFrame(returns_dict).dropna()
    if df.shape[1] < 2 or df.shape[0] < 5:
        return {"error": "Insufficient overlapping data"}
    corr = df.corr()
    matrix = {}
    for t1 in tickers:
        if t1 in corr.columns:
            matrix[t1] = {}
            for t2 in tickers:
                if t2 in corr.columns:
                    val = float(corr.loc[t1, t2])
                    matrix[t1][t2] = round(val, 4)
    return {
        "tickers": [t for t in tickers if t in corr.columns],
        "matrix": matrix,
        "observations": df.shape[0],
        "cat_commentary": "The cat calculated how close these assets dance with each other.",
    }


async def risk_analysis(ticker: str, period: str = "2y", confidence: float = 0.95) -> dict:
    from app.services.analytics.risk import calculate_var
    returns = await _get_returns(ticker, period)
    if returns.empty:
        return {"error": "No return data"}
    var_results = await calculate_var(ticker, confidence)
    if "error" in var_results:
        return var_results
    # Drawdown
    cum_returns = (1 + returns).cumprod()
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max
    max_drawdown = float(drawdown.min()) * 100
    max_drawdown_date = str(drawdown.idxmin().date()) if not drawdown.empty else "N/A"
    # Additional stats
    annual_return = float(returns.mean() * 252 * 100)
    annual_vol = float(returns.std() * np.sqrt(252) * 100)
    sharpe = float(returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
    calmar = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
    skew = float(stats.skew(returns))
    kurt = float(stats.kurtosis(returns))
    return {
        "ticker": ticker,
        "var": var_results.get("var", 0),
        "cvar": var_results.get("cvar", 0),
        "max_drawdown_pct": round(max_drawdown, 2),
        "max_drawdown_date": max_drawdown_date,
        "annual_return_pct": round(annual_return, 2),
        "annual_volatility_pct": round(annual_vol, 2),
        "sharpe_ratio": round(sharpe, 4),
        "calmar_ratio": round(calmar, 4),
        "skewness": round(skew, 4),
        "kurtosis": round(kurt, 4),
        "var_1_day": var_results.get("var_1_day", 0),
        "var_1_week": var_results.get("var_1_week", 0),
        "var_1_month": var_results.get("var_1_month", 0),
        "cat_commentary": f"The cat analyzed your risk. Max drawdown of {abs(max_drawdown):.1f}% is {'😿 concerning' if abs(max_drawdown) > 30 else '😸 manageable' if abs(max_drawdown) > 15 else '😻 low'}. Sharpe {sharpe:.2f} is {'🐟 tuna-worthy' if sharpe > 1 else '🤔 meh'}.",
    }
