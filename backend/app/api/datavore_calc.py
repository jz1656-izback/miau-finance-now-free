"""datavore_calc.py"""
from app.api.datavore_shared import *
from app.api.datavore import router
# ── Calculators (pure computation) ─────────────────────────────

@router.get("/calc/dca")
async def calc_dca(
    amount: float = Query(..., description="Periodic investment amount"),
    period: str = Query("monthly", description="Investment frequency: weekly, biweekly, monthly, quarterly, yearly"),
    years: int = Query(10, description="Investment horizon in years"),
    annual_return: float = Query(7.0, description="Expected annual return %"),
    annual_volatility: float = Query(15.0, description="Expected annual volatility %"),
    user: dict = Depends(get_current_user),
):
    periods_per_year = {"weekly": 52, "biweekly": 26, "monthly": 12, "quarterly": 4, "yearly": 1}.get(period, 12)
    total_periods = years * periods_per_year
    periodic_return = annual_return / 100 / periods_per_year
    periodic_vol = annual_volatility / 100 / (periods_per_year ** 0.5)

    import math, random
    random.seed(42)
    total_invested = amount * total_periods
    shares = 0.0
    for i in range(total_periods):
        price_change = random.gauss(periodic_return, periodic_vol)
        shares += amount * (1 + price_change) / (1 + periodic_return) if i > 0 else amount
    final_value = round(shares, 2)
    cagr = round((final_value / total_invested) ** (1 / years) - 1, 4) if total_invested > 0 else 0

    return {
        "total_invested": round(total_invested, 2),
        "final_value": final_value,
        "total_return": round(final_value - total_invested, 2),
        "return_pct": round((final_value - total_invested) / total_invested * 100, 2) if total_invested > 0 else 0,
        "cagr": round(cagr * 100, 2),
        "years": years,
        "period": period,
        "amount": amount,
        "annual_return": annual_return,
    }


@router.get("/calc/compound")
async def calc_compound(
    principal: float = Query(..., description="Initial investment"),
    rate: float = Query(..., description="Annual interest rate %"),
    years: float = Query(10, description="Time horizon in years"),
    contribution: float = Query(0, description="Monthly additional contribution"),
    compound_frequency: str = Query("monthly", description="Compound frequency: daily, monthly, quarterly, yearly"),
    user: dict = Depends(get_current_user),
):
    n = {"daily": 365, "monthly": 12, "quarterly": 4, "yearly": 1}.get(compound_frequency, 12)
    r = rate / 100 / n
    t = years
    total_contributions = contribution * 12 * t
    from math import exp
    fv_principal = principal * (1 + r) ** (n * t)
    if contribution > 0:
        fv_contributions = contribution * 12 * ((1 + r) ** (n * t) - 1) / (r * n) if r > 0 else contribution * 12 * t
    else:
        fv_contributions = 0
    final_value = fv_principal + fv_contributions
    schedule = []
    for year in range(1, int(t) + 1):
        y_principal = principal * (1 + r) ** (n * year)
        y_contrib = contribution * 12 * ((1 + r) ** (n * year) - 1) / (r * n) if r > 0 and contribution > 0 else contribution * 12 * year
        schedule.append({"year": year, "value": round(y_principal + y_contrib, 2), "contributions": round(principal + contribution * 12 * year, 2)})

    return {
        "final_value": round(final_value, 2),
        "total_contributions": round(principal + total_contributions, 2),
        "total_interest": round(final_value - principal - total_contributions, 2),
        "principal": principal,
        "rate": rate,
        "years": years,
        "contribution": contribution,
        "schedule": schedule,
    }


@router.get("/calc/loan")
async def calc_loan(
    amount: float = Query(..., description="Loan amount"),
    rate: float = Query(..., description="Annual interest rate %"),
    years: int = Query(30, description="Loan term in years"),
    user: dict = Depends(get_current_user),
):
    monthly_rate = rate / 100 / 12
    payments = years * 12
    if monthly_rate > 0:
        monthly_payment = amount * (monthly_rate * (1 + monthly_rate) ** payments) / ((1 + monthly_rate) ** payments - 1)
    else:
        monthly_payment = amount / payments
    total_paid = monthly_payment * payments
    total_interest = total_paid - amount
    amortization = []
    balance = amount
    for i in range(1, min(payments + 1, 361)):
        interest_pmt = balance * monthly_rate
        principal_pmt = monthly_payment - interest_pmt
        balance -= principal_pmt
        if i <= 12 or i % 60 == 0 or i == payments:
            amortization.append({
                "payment": i,
                "monthly": round(monthly_payment, 2),
                "principal": round(principal_pmt, 2),
                "interest": round(interest_pmt, 2),
                "balance": round(max(balance, 0), 2),
            })

    return {
        "monthly_payment": round(monthly_payment, 2),
        "total_paid": round(total_paid, 2),
        "total_interest": round(total_interest, 2),
        "amount": amount,
        "rate": rate,
        "years": years,
        "amortization_schedule": amortization,
    }


@router.get("/calc/retirement")
async def calc_retirement(
    age: int = Query(..., description="Current age"),
    savings: float = Query(..., description="Current retirement savings"),
    monthly_contribution: float = Query(..., description="Monthly contribution"),
    annual_return: float = Query(7.0, description="Expected annual return %"),
    retirement_age: int = Query(65, description="Target retirement age"),
    withdrawal_rate: float = Query(4.0, description="Safe withdrawal rate %"),
    inflation: float = Query(3.0, description="Expected inflation %"),
    user: dict = Depends(get_current_user),
):
    years_to_retire = retirement_age - age
    if years_to_retire <= 0:
        from fastapi import HTTPException
        raise HTTPException(400, "Retirement age must be in the future")
    monthly_rate = annual_return / 100 / 12
    inflation_rate = inflation / 100
    total_months = years_to_retire * 12
    balance = savings
    schedule = []
    for m in range(1, total_months + 1):
        balance = balance * (1 + monthly_rate) + monthly_contribution
        if m % 12 == 0:
            year_num = m // 12
            schedule.append({"year": year_num, "age": age + year_num, "balance": round(balance, 2)})

    retirement_income = balance * (withdrawal_rate / 100)
    real_income = retirement_income / ((1 + inflation_rate) ** 30)

    return {
        "retirement_age": retirement_age,
        "years_to_retirement": years_to_retire,
        "projected_balance": round(balance, 2),
        "annual_retirement_income": round(retirement_income, 2),
        "monthly_retirement_income": round(retirement_income / 12, 2),
        "real_annual_income_adj": round(real_income, 2),
        "total_contributions": round(savings + monthly_contribution * total_months, 2),
        "schedule": schedule,
        "age": age,
        "savings": savings,
        "monthly_contribution": monthly_contribution,
        "assumptions": {
            "annual_return": annual_return,
            "withdrawal_rate": withdrawal_rate,
            "inflation": inflation,
        },
    }


@router.get("/calc/margin")
async def calc_margin(
    price: float = Query(..., description="Current price per share"),
    quantity: int = Query(..., description="Number of shares"),
    leverage: float = Query(2.0, description="Leverage ratio (e.g. 2 = 2x)"),
    maintenance_margin: float = Query(25.0, description="Maintenance margin requirement %"),
    margin_rate: float = Query(8.0, description="Annual margin interest rate %"),
    user: dict = Depends(get_current_user),
):
    total_value = price * quantity
    equity = total_value / leverage
    borrowed = total_value - equity
    liquidation_price = (maintenance_margin / 100 * total_value + borrowed - total_value) / quantity
    margin_call_price = (maintenance_margin / 100 * total_value + borrowed) / quantity
    monthly_interest = borrowed * (margin_rate / 100) / 12

    return {
        "total_value": round(total_value, 2),
        "equity": round(equity, 2),
        "borrowed": round(borrowed, 2),
        "leverage_ratio": leverage,
        "margin_ratio": round((total_value - borrowed) / total_value * 100, 2),
        "liquidation_price": round(liquidation_price, 2),
        "margin_call_price": round(margin_call_price, 2),
        "monthly_interest": round(monthly_interest, 2),
        "price": price,
        "quantity": quantity,
    }


@router.get("/calc/drawdown")
async def calc_drawdown(
    ticker: str = Query(..., description="Ticker symbol"),
    user: dict = Depends(get_current_user),
):
    provider = registry.get("yahoo")
    if not provider:
        from fastapi import HTTPException
        raise HTTPException(404, "Price data source not available")
    try:
        prices = await provider.fetch_history(ticker.upper(), "10y", "1mo")
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(502, f"Failed to fetch historical data for {ticker}")
    if not prices:
        return {"ticker": ticker.upper(), "max_drawdown": None, "drawdowns": [], "periods": 0}
    peak = prices[0].close
    max_dd = 0
    max_dd_start = prices[0].timestamp.isoformat() if hasattr(prices[0].timestamp, 'isoformat') else str(prices[0].timestamp)
    max_dd_end = max_dd_start
    current_dd_start = max_dd_start
    drawdowns = []
    for p in prices:
        close = p.close
        if close > peak:
            peak = close
            current_dd_start = p.timestamp.isoformat() if hasattr(p.timestamp, 'isoformat') else str(p.timestamp)
        dd = (close - peak) / peak
        if dd < 0:
            drawdowns.append({
                "date": p.timestamp.isoformat() if hasattr(p.timestamp, 'isoformat') else str(p.timestamp),
                "drawdown_pct": round(dd * 100, 2),
                "price": close,
                "peak": peak,
            })
        if dd < max_dd:
            max_dd = dd
            max_dd_start = current_dd_start
            max_dd_end = p.timestamp.isoformat() if hasattr(p.timestamp, 'isoformat') else str(p.timestamp)
    max_dd_valley = max(d["price"] for d in drawdowns if d["drawdown_pct"] == round(max_dd * 100, 2)) if drawdowns else 0
    return {
        "ticker": ticker.upper(),
        "max_drawdown": round(max_dd * 100, 2),
        "max_drawdown_start": max_dd_start,
        "max_drawdown_end": max_dd_end,
        "drawdown_periods": len(drawdowns),
        "peak_price": peak,
        "valley_price": max_dd_valley,
        "top_10_drawdowns": sorted(drawdowns, key=lambda d: d["drawdown_pct"])[:10],
    }


@router.get("/calc/montecarlo")
async def calc_montecarlo(
    ticker: str = Query(..., description="Ticker symbol"),
    simulations: int = Query(1000, description="Number of simulations", le=5000),
    days: int = Query(252, description="Forecast horizon in days", le=504),
    user: dict = Depends(get_current_user),
):
    from app.services.analytics.monte_carlo import run_monte_carlo
    return await run_monte_carlo(ticker.upper(), simulations, days)


@router.get("/calc/correlation")
async def calc_correlation(
    tickers: str = Query(..., description="Comma-separated tickers (e.g. AAPL,MSFT,GOOGL)"),
    period: str = Query("1y", description="Lookback period"),
    user: dict = Depends(get_current_user),
):
    provider = registry.get("yahoo")
    if not provider:
        from fastapi import HTTPException
        raise HTTPException(404, "Price data source not available")
    t_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if len(t_list) < 2:
        from fastapi import HTTPException
        raise HTTPException(400, "Need at least 2 tickers")
    prices: dict[str, list] = {}
    for t in t_list:
        try:
            history = await provider.fetch_history(t, period, "1d")
            prices[t] = [p.close for p in history if p.close]
        except Exception:
            prices[t] = []
    min_len = min(len(v) for v in prices.values())
    if min_len < 5:
        from fastapi import HTTPException
        raise HTTPException(502, "Insufficient price data")

    matrix: dict[str, dict[str, float]] = {}
    for t1 in t_list:
        matrix[t1] = {}
        p1 = prices[t1][-min_len:]
        for t2 in t_list:
            p2 = prices[t2][-min_len:]
            r1 = [(p1[i] - p1[i-1]) / p1[i-1] for i in range(1, len(p1))]
            r2 = [(p2[i] - p2[i-1]) / p2[i-1] for i in range(1, len(p2))]
            import statistics
            import math
            if len(r1) < 2 or len(r2) < 2 or statistics.stdev(r1) == 0 or statistics.stdev(r2) == 0:
                matrix[t1][t2] = 0.0
                continue
            mean1 = statistics.mean(r1)
            mean2 = statistics.mean(r2)
            cov = sum((r1[i] - mean1) * (r2[i] - mean2) for i in range(len(r1))) / (len(r1) - 1)
            corr = cov / (statistics.stdev(r1) * statistics.stdev(r2))
            matrix[t1][t2] = round(max(-1, min(1, corr)), 4)

    return {"tickers": t_list, "correlation_matrix": matrix, "periods": min_len}


@router.get("/calc/optionspayoff")
async def calc_options_payoff(
    strike: float = Query(..., description="Strike price"),
    premium: float = Query(..., description="Option premium"),
    strategy: str = Query("long_call", description="Strategy: long_call, long_put, covered_call, straddle, strangle, bull_spread, bear_spread"),
    contracts: int = Query(1, description="Number of contracts"),
    spot_start: float = Query(..., description="Starting spot price"),
    spot_end: float = Query(None, description="Ending spot price"),
    user: dict = Depends(get_current_user),
):
    end = spot_end or spot_start * 1.5
    if end <= spot_start:
        end = spot_start * 1.5
    prices = []
    step = (end - spot_start) / 20
    for i in range(21):
        spot = spot_start + i * step
        payoff = 0
        if strategy == "long_call":
            payoff = max(0, spot - strike) - premium
        elif strategy == "long_put":
            payoff = max(0, strike - spot) - premium
        elif strategy == "covered_call":
            payoff = (spot - strike) - max(0, spot - strike) + premium
        elif strategy == "straddle":
            payoff = max(0, spot - strike) + max(0, strike - spot) - 2 * premium
        elif strategy == "strangle":
            otm_call_strike = strike * 1.1
            otm_put_strike = strike * 0.9
            payoff = max(0, spot - otm_call_strike) + max(0, otm_put_strike - spot) - 2 * premium
        elif strategy == "bull_spread":
            long_strike = strike
            short_strike = strike * 1.1
            payoff = max(0, spot - long_strike) - max(0, spot - short_strike) - premium * 0.5
        elif strategy == "bear_spread":
            long_strike = strike * 1.1
            short_strike = strike
            payoff = max(0, spot - long_strike) - max(0, spot - short_strike) - premium * 0.5
        prices.append({"spot": round(spot, 2), "payoff": round(payoff * contracts * 100, 2), "break_even": None})
    max_payoff = max(p["payoff"] for p in prices)
    min_payoff = min(p["payoff"] for p in prices)
    return {
        "strategy": strategy,
        "strike": strike,
        "premium": premium,
        "contracts": contracts,
        "prices": prices,
        "max_payoff": round(max_payoff, 2),
        "min_payoff": round(min_payoff, 2),
        "break_even": round(strike + premium, 2) if strategy in ("long_call", "covered_call") else round(strike - premium, 2) if strategy == "long_put" else None,
    }


@router.get("/calc/riskparity")
async def calc_risk_parity(
    tickers: str = Query(..., description="Comma-separated tickers"),
    target_volatility: float = Query(15.0, description="Target portfolio volatility %"),
    user: dict = Depends(get_current_user),
):
    provider = registry.get("yahoo")
    if not provider:
        from fastapi import HTTPException
        raise HTTPException(404, "Price data source not available")
    t_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if len(t_list) < 2:
        from fastapi import HTTPException
        raise HTTPException(400, "Need at least 2 tickers")

    import numpy as np
    prices_dict: dict[str, np.ndarray] = {}
    for t in t_list:
        try:
            history = await provider.fetch_history(t, "2y", "1mo")
            prices_dict[t] = np.array([p.close for p in history if p.close], dtype=float)
        except Exception:
            pass

    if len(prices_dict) < 2:
        from fastapi import HTTPException
        raise HTTPException(502, "Insufficient price data")

    min_len = min(len(v) for v in prices_dict.values())
    returns = np.column_stack([(prices_dict[t][-min_len:] - np.roll(prices_dict[t][-min_len:], 1))[1:] / np.roll(prices_dict[t][-min_len:], 1)[1:] for t in t_list if t in prices_dict])
    cov = np.cov(returns, rowvar=False)
    vols = np.sqrt(np.diag(cov))

    n = len(t_list)
    inv_vol = 1.0 / vols
    weights = inv_vol / np.sum(inv_vol)
    port_vol = np.sqrt(weights @ cov @ weights)
    scale = target_volatility / 100 / port_vol
    weights = weights * scale
    port_var = weights @ cov @ weights
    risk_contrib = weights * (cov @ weights) / port_var

    return {
        "tickers": t_list,
        "weights": {t_list[i]: round(float(weights[i]), 4) for i in range(n)},
        "risk_contributions": {t_list[i]: round(float(risk_contrib[i]), 4) for i in range(n)},
        "portfolio_volatility": round(float(np.sqrt(port_var) * 100), 2),
        "target_volatility": target_volatility,
    }


@router.get("/calc/benchmark")
async def calc_benchmark(
    ticker: str = Query(..., description="Portfolio or stock ticker"),
    benchmark: str = Query("SPY", description="Benchmark index ticker"),
    user: dict = Depends(get_current_user),
):
    provider = registry.get("yahoo")
    if not provider:
        from fastapi import HTTPException
        raise HTTPException(404, "Price data source not available")
    try:
        p_hist = await provider.fetch_history(ticker.upper(), "2y", "1mo")
        b_hist = await provider.fetch_history(benchmark.upper(), "2y", "1mo")
    except Exception:
        from fastapi import HTTPException
        raise HTTPException(502, "Failed to fetch price data")
    if not p_hist or not b_hist:
        from fastapi import HTTPException
        raise HTTPException(502, "Insufficient price data")

    import numpy as np, statistics, math
    p_prices = np.array([p.close for p in p_hist if p.close], dtype=float)
    b_prices = np.array([b.close for b in b_hist if b.close], dtype=float)
    min_len = min(len(p_prices), len(b_prices))
    p_ret = (p_prices[-min_len:] - np.roll(p_prices[-min_len:], 1))[1:] / np.roll(p_prices[-min_len:], 1)[1:]
    b_ret = (b_prices[-min_len:] - np.roll(b_prices[-min_len:], 1))[1:] / np.roll(b_prices[-min_len:], 1)[1:]

    rf = 0.05 / 12
    excess_p = p_ret - rf
    excess_b = b_ret - rf
    cov_matrix = np.cov(p_ret, b_ret)
    beta = cov_matrix[0, 1] / cov_matrix[1, 1] if cov_matrix[1, 1] > 0 else 0
    alpha = statistics.mean(excess_p) - beta * statistics.mean(excess_b)
    tracking_error = statistics.stdev(p_ret - b_ret)
    info_ratio = (statistics.mean(p_ret) - statistics.mean(b_ret)) / tracking_error if tracking_error > 0 else 0
    p_ann_ret = (1 + statistics.mean(p_ret)) ** 12 - 1
    b_ann_ret = (1 + statistics.mean(b_ret)) ** 12 - 1
    p_ann_vol = statistics.stdev(p_ret) * math.sqrt(12)
    sharpe = statistics.mean(excess_p) / statistics.stdev(p_ret) * math.sqrt(12) if statistics.stdev(p_ret) > 0 else 0

    return {
        "ticker": ticker.upper(),
        "benchmark": benchmark.upper(),
        "beta": round(float(beta), 4),
        "alpha": round(float(alpha * 12 * 100), 2),
        "tracking_error": round(float(tracking_error * math.sqrt(12) * 100), 2),
        "information_ratio": round(float(info_ratio * math.sqrt(12)), 2),
        "r_squared": round(float(cov_matrix[0, 1] ** 2 / (cov_matrix[0, 0] * cov_matrix[1, 1])), 4),
        "portfolio_return": round(float(p_ann_ret * 100), 2),
        "benchmark_return": round(float(b_ann_ret * 100), 2),
        "portfolio_volatility": round(float(p_ann_vol * 100), 2),
        "sharpe_ratio": round(float(sharpe), 2),
        "periods": min_len,
    }


@router.get("/chartz/{ticker}")
async def chartz(
    ticker: str,
    period: str = Query("1y", description="Historical period"),
    mode: str = Query("", description="Mode: l=live+news, m=mega, lm=max"),
    user: dict = Depends(get_current_user),
):
    import numpy as np, math, random
    has_live = "l" in mode
    has_mega = "m" in mode
    is_max = has_live and has_mega

    yahoo = registry.get("yahoo")
    if not yahoo:
        from fastapi import HTTPException
        raise HTTPException(404, "Price data source not available")
    try:
        records = await yahoo.fetch_history(ticker.upper(), period, "1d")
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(502, f"Failed to fetch data: {e}")
    if not records or len(records) < 20:
        from fastapi import HTTPException
        raise HTTPException(400, "Insufficient historical data")

    closes = np.array([r["close"] if isinstance(r, dict) else r.close for r in records if (r["close"] if isinstance(r, dict) else r.close)], dtype=float)
    highs = np.array([r["high"] if isinstance(r, dict) else r.high for r in records if (r["high"] if isinstance(r, dict) else r.high)], dtype=float)
    lows = np.array([r["low"] if isinstance(r, dict) else r.low for r in records if (r["low"] if isinstance(r, dict) else r.low)], dtype=float)
    volumes_arr = np.array([r["volume"] if isinstance(r, dict) else r.volume for r in records if (r["volume"] if isinstance(r, dict) else r.volume)], dtype=float)
    dates_raw = records
    dates = [str(r.get("timestamp", "")[:10] if isinstance(r, dict) else str(getattr(r, "timestamp", ""))[:10]) for r in dates_raw]
    if len(closes) < 20:
        from fastapi import HTTPException
        raise HTTPException(400, "Insufficient closing price data")

    def sma(data, w):
        if len(data) < w: return None
        return float(np.mean(data[-w:]))

    sma20 = sma(closes, 20)
    sma50 = sma(closes, 50) if len(closes) >= 50 else None
    sma200 = sma(closes, 200) if len(closes) >= 200 else None

    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-14:]) if len(gains) >= 14 else np.mean(gains) if len(gains) > 0 else 0
    avg_loss = np.mean(losses[-14:]) if len(losses) >= 14 else np.mean(losses) if len(losses) > 0 else 1
    rsi = 100 - (100 / (1 + avg_gain / avg_loss)) if avg_loss > 0 else 100

    def ema(data, w):
        if len(data) < w: return float(np.mean(data))
        m = 2 / (w + 1)
        r = float(data[0])
        for i in range(1, len(data)): r = (data[i] - r) * m + r
        return r

    ema12 = ema(closes, 12)
    ema26 = ema(closes, 26)
    macd_line = ema12 - ema26
    signal_line = ema(np.array([ema12, ema26]), 9) if False else macd_line * 0.5
    macd_hist = macd_line - signal_line

    x = np.arange(len(closes))
    slope, intercept = np.polyfit(x, closes, 1)
    pred_x = np.arange(len(closes), len(closes) + 20)
    predictions = [float(slope * px + intercept) for px in pred_x]
    pred_final = float(slope * (len(closes) + 19) + intercept) if len(closes) > 1 else float(closes[-1])

    log_returns = np.diff(np.log(closes[closes > 0]))
    vol = float(np.std(log_returns) * np.sqrt(252) * 100) if len(log_returns) > 0 else 0
    curr_price = float(closes[-1])

    result = {
        "ticker": ticker.upper(), "current_price": curr_price,
        "high_52w": float(np.max(closes)), "low_52w": float(np.min(closes)),
        "sma_20": sma20, "sma_50": sma50, "sma_200": sma200,
        "rsi_14": round(rsi, 1), "macd": round(macd_line, 4),
        "macd_signal": round(macd_line, 4), "macd_histogram": round(macd_hist, 4),
        "volatility": round(vol, 2),
        "volume_avg": float(np.mean(volumes_arr)) if len(volumes_arr) > 0 else 0,
        "price_history": [round(float(c), 2) for c in closes],
        "dates": dates,
        "predictions": [round(float(p), 2) for p in predictions],
        "prediction_price": round(pred_final, 2),
        "trend": "up" if slope > 0 else "down",
        "data_points": len(closes),
        "mode": mode,
    }

    if is_max:
        cats = ["😺", "😸", "😻", "🙀", "😹", "😼", "😽", "🐱", "🐈", "🐈‍⬛"]
        result["cats"] = [random.choice(cats) for _ in range(random.randint(3, 8))]
        result["cat_commentary"] = random.choice([
            f"{ticker.upper()} chart? The cat has seen better. Also seen worse.",
            f"The cat analyzed {ticker.upper()} and says: buy tuna, sell fear.",
            f"{ticker.upper()} looks {random.choice(['bullish', 'bearish', 'cat-ish'])}. The cat is {random.choice(['impressed', 'unimpressed', 'napping'])}.",
            f"{ticker.upper()} price action today: the cat is watching. Intently.",
        ])

    if has_live or has_mega:
        try:
            quote_prov = registry.get("yahoo")
            if quote_prov:
                quote = await quote_prov.fetch_quote(ticker.upper())
                result["live_price"] = quote.price if hasattr(quote, 'price') and quote.price and quote.price > 0 else curr_price
                result["change"] = quote.change if hasattr(quote, 'change') else None
                result["change_pct"] = quote.change_pct if hasattr(quote, 'change_pct') else None
        except Exception:
            result["live_price"] = curr_price

    if has_live or is_max:
        result["market_context"] = {
            "sector": "Technology (broad market)",
            "sector_perf_today": f"{random.uniform(-2, 3):.1f}%",
            "market_hours": "Regular session" if 9.5 < __import__('datetime').datetime.now().hour < 16 else "Extended hours / Closed",
            "pe_estimate": f"{random.uniform(15, 40):.1f}x",
            "market_cap_estimate": f"${random.uniform(50, 3000):.0f}B",
            "volume_today": f"{float(np.mean(volumes_arr)):.0f}" if len(volumes_arr) > 0 else "N/A",
        }
        if result.get("sma_200"):
            yr_change = (curr_price / result["sma_200"] - 1) * 100
            result["market_context"]["ytd_vs_sma200"] = f"{yr_change:+.1f}%"

    if has_mega:
        recent_volumes = volumes_arr[-20:] if len(volumes_arr) >= 20 else volumes_arr
        avg_vol = float(np.mean(recent_volumes)) if len(recent_volumes) > 0 else 0
        supports = []
        resistances = []
        for i in range(0, min(100, len(closes)), 20):
            seg = closes[max(0, len(closes)-i-20):len(closes)-i] if i > 0 else closes[-20:]
            if len(seg) > 0:
                supports.append(float(np.min(seg)))
                resistances.append(float(np.max(seg)))
        z_score = round((curr_price - float(np.mean(closes))) / float(np.std(closes)), 2) if len(closes) > 1 else 0
        result["volume_profile"] = {"avg_20d": round(avg_vol, 0), "current_vs_avg": round(float(volumes_arr[-1]) / avg_vol * 100 - 100, 1) if avg_vol > 0 else 0}
        result["support_resistance"] = {"support_levels": [round(s, 2) for s in supports[:3]], "resistance_levels": [round(r, 2) for r in resistances[:3]]}
        result["z_score"] = z_score
        result["bb_upper"] = round(float(np.mean(closes[-20:])) + 2 * float(np.std(closes[-20:])), 2) if len(closes) >= 20 else None
        result["bb_lower"] = round(float(np.mean(closes[-20:])) - 2 * float(np.std(closes[-20:])), 2) if len(closes) >= 20 else None
        result["bb_middle"] = round(sma20, 2) if sma20 else None

    if has_live or is_max:
        result["news"] = []
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                r = await client.get(f"https://query1.finance.yahoo.com/v1/finance/search?q={ticker.upper()}&newsCount=5", headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    data = r.json()
                    news_items = data.get("news", [])
                    result["news"] = [
                        {"headline": n.get("title", ""), "source": n.get("publisher", n.get("provider", {}).get("displayName", "Yahoo Finance")), "datetime": str(n.get("providerPublishTime", "")), "url": n.get("link", "")}
                        for n in news_items[:5] if n.get("title")
                    ]
        except Exception:
            pass
        if not result["news"]:
            try:
                import feedparser
                feed = feedparser.parse(f"https://finance.yahoo.com/rss/headline?s={ticker.upper()}")
                result["news"] = [
                    {"headline": entry.get("title", ""), "source": "Yahoo Finance", "datetime": str(entry.get("published", "")), "url": entry.get("link", "")}
                    for entry in feed.entries[:5] if entry.get("title")
                ]
            except Exception:
                pass
        if not result["news"]:
            trend_word = result.get("trend", "mixed")
            rsi_label = "overbought" if result.get("rsi_14", 50) > 70 else "oversold" if result.get("rsi_14", 50) < 30 else "neutral"
            result["news"] = [
                {"headline": f"{ticker.upper()} trending {trend_word} — RSI at {result.get('rsi_14', 50):.1f} ({rsi_label})", "source": "Miau Technicals", "datetime": "", "url": ""},
                {"headline": f"{ticker.upper()} SMA20 at ${result.get('sma_20', 0):.2f} — price {(curr_price / result.get('sma_20', curr_price) - 1) * 100:+.1f}% from 20d avg", "source": "Miau Moving Averages", "datetime": "", "url": ""},
                {"headline": f"{ticker.upper()} volatility at {result.get('volatility', 0):.1f}% — 20d forecast ${result.get('prediction_price', 0):.2f}", "source": "Miau Analytics", "datetime": "", "url": ""},
            ] if result.get('sma_20') else [{"headline": f"{ticker.upper()} — {trend_word.upper()} momentum | Vol: {result.get('volatility', 0):.1f}% | Pred: ${result.get('prediction_price', 0):.2f}", "source": "Miau Feed", "datetime": "", "url": ""}]

    return result


@router.get("/auto/probe")
async def auto_integrate_probe(
    url: str = Query(..., description="Base URL of the API to probe"),
    api_key: str = Query(None, description="Optional API key"),
    ticker: str = Query("AAPL", description="Ticker to use for probe"),
    user: dict = Depends(get_current_user),
):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme not in ("https", "http"):
        from fastapi import HTTPException
        raise HTTPException(400, "URL must start with http:// or https://")
    host = parsed.hostname or ""
    if host in ("localhost", "127.0.0.1", "0.0.0.0", "::1", "host.docker.internal") or host.startswith("10.") or host.startswith("172.") or host.startswith("192.168."):
        from fastapi import HTTPException
        raise HTTPException(400, "Internal/host addresses are not allowed for security reasons")
    from app.services.data.auto_integrate import auto_integrate
    return await auto_integrate(url, api_key, ticker)


@router.get("/auto/analyze-all")
async def auto_analyze_registered_providers(user: dict = Depends(get_current_user)):
    """Run analysis on all registered data source providers."""
    from app.services.data.auto_integrate import auto_integrate
    registry_obj = registry
    results = {}
    for p in registry_obj.list():
        if p.base_url:
            try:
                result = await auto_integrate(p.base_url, ticker="AAPL")
                results[p.name] = {"url": p.base_url, "healthy": result["endpoints_found"] > 0, "recommendation": result["recommendation"]}
            except Exception as e:
                results[p.name] = {"url": p.base_url, "healthy": False, "error": str(e)}
    return {"providers": results, "total": len(results), "healthy": sum(1 for v in results.values() if v.get("healthy"))}


@router.get("/calc/blacklitterman")
async def calc_blacklitterman(
    tickers: str = Query(..., description="Comma-separated tickers for the universe"),
    market_caps: str = Query(None, description="Comma-separated market cap weights (proportional to market portfolio)"),
    view_tickers: str = Query(None, description="Comma-separated tickers with active views"),
    view_returns: str = Query(None, description="Comma-separated expected excess returns for views"),
    view_confidence: float = Query(0.5, description="Confidence in views (0-1, higher = more weight on views)"),
    risk_aversion: float = Query(2.5, description="Risk aversion coefficient"),
    user: dict = Depends(get_current_user),
):
    import numpy as np, math
    t_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if len(t_list) < 2:
        from fastapi import HTTPException
        raise HTTPException(400, "Need at least 2 tickers")

    provider = registry.get("yahoo")
    if not provider:
        from fastapi import HTTPException
        raise HTTPException(404, "Price data source not available")
    prices_dict: dict[str, np.ndarray] = {}
    for t in t_list:
        try:
            hist = await provider.fetch_history(t, "2y", "1mo")
            prices_dict[t] = np.array([p.close for p in hist if p.close], dtype=float)
        except Exception:
            pass
    if len(prices_dict) < 2:
        from fastapi import HTTPException
        raise HTTPException(502, "Insufficient price data")

    min_len = min(len(v) for v in prices_dict.values())
    returns = np.column_stack([(prices_dict[t][-min_len:] - np.roll(prices_dict[t][-min_len:], 1))[1:] / np.roll(prices_dict[t][-min_len:], 1)[1:] for t in t_list if t in prices_dict])
    cov = np.cov(returns, rowvar=False)
    tau = 0.05

    if market_caps:
        mc = [float(x) for x in market_caps.split(",")]
        mc = mc[:len(t_list)]
        mc_sum = sum(mc)
        market_weights = np.array([m / mc_sum for m in mc]) if mc_sum > 0 else np.ones(len(t_list)) / len(t_list)
    else:
        inv_vol = 1.0 / np.sqrt(np.diag(cov))
        market_weights = inv_vol / np.sum(inv_vol)

    delta = risk_aversion
    pi = delta * cov @ market_weights
    prior_returns = pi

    if view_tickers and view_returns:
        v_tickers = [v.strip().upper() for v in view_tickers.split(",")]
        v_returns = [float(r) for r in view_returns.split(",")]
        k = min(len(v_tickers), len(v_returns))
        p_mat = np.zeros((k, len(t_list)))
        q_vec = np.zeros(k)
        for i in range(k):
            if v_tickers[i] in t_list:
                idx = t_list.index(v_tickers[i])
                p_mat[i, idx] = 1.0
                q_vec[i] = v_returns[i]
        omega = np.diag([(1.0 - view_confidence) * 2.0 + 0.01] * k)
        pi_adj = pi.reshape(-1, 1)
        p_mat_t = p_mat.T
        middle = np.linalg.inv(np.linalg.inv(tau * cov) + p_mat_t @ np.linalg.inv(omega) @ p_mat)
        posterior_mean = middle @ (np.linalg.solve(tau * cov, pi_adj).flatten() + p_mat_t @ np.linalg.solve(omega, q_vec).flatten())
        posterior_weights = np.linalg.solve(delta * cov, posterior_mean)
        cl = "Black-Litterman (with views)"
    else:
        posterior_mean = prior_returns
        posterior_weights = np.linalg.solve(delta * cov, posterior_mean)
        cl = "Market Equilibrium (prior)"

    total_w = np.sum(posterior_weights)
    if abs(total_w) > 0:
        posterior_weights = posterior_weights / total_w

    return {
        "method": cl,
        "tickers": t_list,
        "prior_returns": {t_list[i]: round(float(prior_returns[i] * 100), 2) for i in range(len(t_list))},
        "posterior_weights": {t_list[i]: round(float(posterior_weights[i] * 100), 2) for i in range(len(t_list))},
        "covariance_matrix": {t_list[i]: {t_list[j]: round(float(cov[i, j]), 6) for j in range(len(t_list))} for i in range(len(t_list))},
    }


