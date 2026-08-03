import numpy as np
import pandas as pd
import math
from datetime import datetime
from typing import Optional
from app.services.analytics._yf import get_history


def _clean(obj):
    if isinstance(obj, float):
        return None if math.isnan(obj) or math.isinf(obj) else obj
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean(v) for v in obj]
    return obj


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


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "Close" not in df.columns:
        return df
    close = df["Close"].dropna().values
    if len(close) < 20:
        return df

    # SMA
    df["SMA_20"] = pd.Series(close).rolling(20).mean().values
    df["SMA_50"] = pd.Series(close).rolling(50).mean().values if len(close) >= 50 else float("nan")
    df["SMA_200"] = pd.Series(close).rolling(200).mean().values if len(close) >= 200 else float("nan")

    # EMA
    df["EMA_12"] = pd.Series(close).ewm(span=12).mean().values
    df["EMA_26"] = pd.Series(close).ewm(span=26).mean().values

    # MACD
    macd = pd.Series(close).ewm(span=12).mean() - pd.Series(close).ewm(span=26).mean()
    df["MACD"] = macd.values
    df["MACD_Signal"] = macd.ewm(span=9).mean().values
    df["MACD_Hist"] = (df["MACD"] - df["MACD_Signal"]).values

    # RSI
    delta = pd.Series(close).diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df["RSI_14"] = (100 - (100 / (1 + rs))).values

    # Bollinger
    sma20 = pd.Series(close).rolling(20).mean()
    std20 = pd.Series(close).rolling(20).std()
    df["BB_Upper"] = (sma20 + 2 * std20).values
    df["BB_Lower"] = (sma20 - 2 * std20).values

    # ATR
    if "High" in df.columns and "Low" in df.columns:
        tr = pd.DataFrame({
            "hl": df["High"].values - df["Low"].values,
            "hc": np.abs(df["High"].values - np.roll(close, 1)),
            "lc": np.abs(df["Low"].values - np.roll(close, 1)),
        }).max(axis=1)
        df["ATR_14"] = tr.rolling(14).mean().values

    # OBV
    if "Volume" in df.columns:
        obv = (np.sign(close - np.roll(close, 1)) * df["Volume"].values).cumsum()
        df["OBV"] = obv

    return df


async def generate_signals(ticker: str, period: str = "6mo") -> dict:
    range_map = {"1mo": "1mo", "3mo": "3mo", "6mo": "6mo", "1y": "1y", "2y": "2y"}
    yf_range = range_map.get(period, "6mo")
    records = await get_history(ticker, yf_range)

    if not records:
        return {"ticker": ticker, "error": "No data", "signals": []}

    df = _hist_to_df(records)
    if df.empty:
        return {"ticker": ticker, "error": "Empty data", "signals": []}

    df = calculate_indicators(df)
    signals = []
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    price = float(last["Close"]) if "Close" in last else 0

    # SMA crossover
    if "SMA_20" in last and "SMA_50" in last and not (pd.isna(last["SMA_20"]) or pd.isna(last["SMA_50"])):
        if prev["SMA_20"] <= prev["SMA_50"] and last["SMA_20"] > last["SMA_50"]:
            signals.append({"type": "BUY", "indicator": "SMA Crossover", "detail": "SMA20 crossed above SMA50", "strength": "strong"})
        elif prev["SMA_20"] >= prev["SMA_50"] and last["SMA_20"] < last["SMA_50"]:
            signals.append({"type": "SELL", "indicator": "SMA Crossover", "detail": "SMA20 crossed below SMA50", "strength": "strong"})

    # MACD
    if "MACD" in last and "MACD_Signal" in last and not (pd.isna(last["MACD"]) or pd.isna(last["MACD_Signal"])):
        if prev["MACD"] <= prev["MACD_Signal"] and last["MACD"] > last["MACD_Signal"]:
            signals.append({"type": "BUY", "indicator": "MACD", "detail": "MACD crossed above signal", "strength": "moderate"})
        elif prev["MACD"] >= prev["MACD_Signal"] and last["MACD"] < last["MACD_Signal"]:
            signals.append({"type": "SELL", "indicator": "MACD", "detail": "MACD crossed below signal", "strength": "moderate"})

    # RSI
    if "RSI_14" in last and not pd.isna(last["RSI_14"]):
        rsi_val = last["RSI_14"]
        if rsi_val < 30:
            signals.append({"type": "BUY", "indicator": "RSI", "detail": f"Oversold ({rsi_val:.0f})", "strength": "strong"})
        elif rsi_val > 70:
            signals.append({"type": "SELL", "indicator": "RSI", "detail": f"Overbought ({rsi_val:.0f})", "strength": "strong"})
        elif rsi_val < 40:
            signals.append({"type": "BUY", "indicator": "RSI", "detail": f"Approaching oversold ({rsi_val:.0f})", "strength": "weak"})
        elif rsi_val > 60:
            signals.append({"type": "SELL", "indicator": "RSI", "detail": f"Approaching overbought ({rsi_val:.0f})", "strength": "weak"})

    # Bollinger
    if "BB_Upper" in last and "BB_Lower" in last:
        if not pd.isna(last["BB_Upper"]) and not pd.isna(last["BB_Lower"]):
            if price > last["BB_Upper"]:
                signals.append({"type": "SELL", "indicator": "Bollinger", "detail": "Price above upper band", "strength": "moderate"})
            elif price < last["BB_Lower"]:
                signals.append({"type": "BUY", "indicator": "Bollinger", "detail": "Price below lower band", "strength": "moderate"})

    # Trend
    trend = "neutral"
    if "SMA_50" in last and "SMA_200" in last:
        if not (pd.isna(last["SMA_50"]) or pd.isna(last["SMA_200"])):
            if last["SMA_50"] > last["SMA_200"] and price > last["SMA_50"]:
                trend = "bullish"
            elif last["SMA_50"] < last["SMA_200"] and price < last["SMA_50"]:
                trend = "bearish"

    indicators = {}
    for k in ["RSI_14", "MACD", "MACD_Signal", "SMA_20", "SMA_50", "BB_Upper", "BB_Lower", "ATR_14"]:
        if k in last and not pd.isna(last[k]):
            indicators[k.lower()] = round(float(last[k]), 4)

    return _clean({
        "ticker": ticker,
        "price": price,
        "trend": trend,
        "signals": signals,
        "indicators": indicators,
        "data": df.tail(100).reset_index().to_dict(orient="records"),
    })


async def backtest_strategy(
    ticker: str, strategy: str = "sma_cross",
    short_window: int = 20, long_window: int = 50,
    initial_capital: float = 100000, period: str = "1y",
) -> dict:
    records = await get_history(ticker, period)
    if not records:
        return {"ticker": ticker, "error": "Insufficient data"}

    df = _hist_to_df(records)
    if df.empty or len(df) < long_window:
        return {"ticker": ticker, "error": "Insufficient data"}

    df["SMA_short"] = df["Close"].rolling(short_window).mean()
    df["SMA_long"] = df["Close"].rolling(long_window).mean()

    if strategy == "sma_cross":
        df["Signal"] = 0
        df.loc[df["SMA_short"] > df["SMA_long"], "Signal"] = 1
        df["Position"] = df["Signal"].diff()
    elif strategy == "rsi":
        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        df["Signal"] = 0
        df.loc[df["RSI"] < 30, "Signal"] = 1
        df.loc[df["RSI"] > 70, "Signal"] = 0
        df["Position"] = df["Signal"].diff()
    else:
        return {"error": f"Unknown strategy: {strategy}"}

    df = df.dropna()
    if df.empty:
        return {"ticker": ticker, "error": "No data after indicators"}

    df["Market_Return"] = df["Close"].pct_change()
    df["Strategy_Return"] = df["Signal"].shift(1) * df["Market_Return"]

    df["Market_Equity"] = (1 + df["Market_Return"].fillna(0)).cumprod() * initial_capital
    df["Strategy_Equity"] = (1 + df["Strategy_Return"].fillna(0)).cumprod() * initial_capital

    total_market_return = (df["Market_Equity"].iloc[-1] / initial_capital - 1) * 100
    total_strategy_return = (df["Strategy_Equity"].iloc[-1] / initial_capital - 1) * 100

    trades = []
    for i in range(1, len(df)):
        if df["Position"].iloc[i] != 0:
            pos = df["Position"].iloc[i]
            trades.append({
                "date": str(df.index[i].date()),
                "action": "BUY" if pos == 1 else "SELL",
                "price": round(float(df["Close"].iloc[i]), 2),
            })

    winning_days = len(df[df["Strategy_Return"] > 0])
    total_days = len(df[df["Strategy_Return"] != 0])
    win_rate = winning_days / total_days * 100 if total_days > 0 else 0

    cum_max = df["Strategy_Equity"].cummax()
    drawdown = (df["Strategy_Equity"] - cum_max) / cum_max
    max_dd = float(drawdown.min() * 100)

    strategy_returns = df["Strategy_Return"].dropna()
    sharpe = float(np.sqrt(252) * strategy_returns.mean() / strategy_returns.std()) if strategy_returns.std() > 0 else 0

    return _clean({
        "ticker": ticker,
        "strategy": strategy,
        "parameters": {"short_window": short_window, "long_window": long_window},
        "initial_capital": initial_capital,
        "final_capital": round(float(df["Strategy_Equity"].iloc[-1]), 2),
        "total_return_pct": round(float(total_strategy_return), 2),
        "buy_and_hold_return_pct": round(float(total_market_return), 2),
        "outperformance_pct": round(float(total_strategy_return - total_market_return), 2),
        "sharpe_ratio": round(float(sharpe), 4),
        "max_drawdown_pct": round(float(max_dd), 2),
        "win_rate_pct": round(float(win_rate), 2),
        "num_trades": len(trades),
        "trades": trades[:50],
        "equity_curve": [
            {"date": str(k.date()), "strategy": round(float(v), 2), "buy_hold": round(float(df["Market_Equity"].iloc[i]), 2)}
            for i, (k, v) in enumerate(df["Strategy_Equity"].items())
        ][::5],
    })
