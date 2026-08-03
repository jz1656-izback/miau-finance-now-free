import numpy as np
from datetime import datetime
from app.services.analytics._yf import get_history

try:
    from miau_analytics import run_monte_carlo_gbm as _rust_mc

    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False


async def run_monte_carlo(
    ticker: str,
    num_simulations: int = 1000,
    days: int = 252,
    period: str = "2y",
) -> dict:
    records = await get_history(ticker, period)
    if not records or len(records) < 20:
        return {"error": "Insufficient historical data"}

    closes = [r["close"] for r in records if r.get("close")]
    if len(closes) < 20:
        return {"error": "Insufficient closing price data"}

    prices = np.array(closes, dtype=float)
    log_returns = np.diff(np.log(prices))
    mu = np.mean(log_returns) * 252
    sigma = np.std(log_returns) * np.sqrt(252)
    last_price = float(prices[-1])

    if _HAS_RUST:
        result = _rust_mc(
            last_price=last_price,
            mu=mu,
            sigma=sigma,
            num_simulations=num_simulations,
            days=days,
            seed=42,
        )
        final_prices = np.asarray(result["final_prices"])
        histogram = result["histogram"]
        path_sample = result["path_sample"]
        sampled_days = result["sampled_days"]
        summary = result["summary"]
        probability = result["probability"]
        var = result["value_at_risk"]
    else:
        dt = 1 / 252
        rng = np.random.default_rng(42)
        rand = rng.standard_normal((num_simulations, days))

        simulated = np.zeros((days + 1, num_simulations))
        simulated[0, :] = last_price
        drift = (mu - 0.5 * sigma**2) * dt
        vol = sigma * np.sqrt(dt)
        for i in range(1, days + 1):
            simulated[i, :] = simulated[i - 1, :] * np.exp(drift + vol * rand[:, i - 1])

        final_prices = simulated[-1, :]

        hist, bin_edges = np.histogram(final_prices, bins=30)
        histogram = [
            {"bin_start": round(float(bin_edges[i]), 2), "bin_end": round(float(bin_edges[i + 1]), 2), "count": int(hist[i])}
            for i in range(len(hist))
        ]
        path_sample = simulated[:10, :].T.tolist()
        sampled_days = [round(float(np.mean(simulated[d, :])), 2) for d in range(0, days + 1, max(1, days // 20))]

        mean_final = float(np.mean(final_prices))
        std_final = float(np.std(final_prices))
        median_final = float(np.median(final_prices))
        prob_profit = float(np.mean(final_prices > last_price))
        prob_loss = float(np.mean(final_prices < last_price))
        var_95 = float(np.percentile(final_prices, 5))
        var_99 = float(np.percentile(final_prices, 1))
        cvar_95 = float(np.mean(final_prices[final_prices <= var_95])) if np.any(final_prices <= var_95) else var_95

        summary = {
            "mean_final_price": round(mean_final, 2),
            "median_final_price": round(median_final, 2),
            "std_final_price": round(std_final, 2),
            "min_final_price": round(float(np.min(final_prices)), 2),
            "max_final_price": round(float(np.max(final_prices)), 2),
        }
        probability = {"profit": round(prob_profit, 4), "loss": round(prob_loss, 4)}
        var = {"var_95": round(var_95, 2), "var_99": round(var_99, 2), "cvar_95": round(cvar_95, 2)}

    return {
        "ticker": ticker,
        "num_simulations": num_simulations,
        "days": days,
        "last_price": round(last_price, 2),
        "mu": round(float(mu), 6),
        "sigma": round(float(sigma), 6),
        "summary": summary,
        "probability": probability,
        "value_at_risk": var,
        "histogram": histogram,
        "path_sample": path_sample,
        "sampled_days": sampled_days,
        "as_of": datetime.now().isoformat(),
    }
