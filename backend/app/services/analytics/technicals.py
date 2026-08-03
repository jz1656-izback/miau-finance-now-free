"""Technical Analysis engine — 17 indicators, candlestick patterns, buy/sell signals."""
import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
from typing import Optional
from app.services.analytics._yf import get_history


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


def _clean(val):
    if isinstance(val, (float, np.floating)):
        return None if (np.isnan(val) or np.isinf(val)) else float(round(val, 4))
    if isinstance(val, np.integer):
        return int(val)
    return val


def rsi(close: np.ndarray, period: int = 14) -> np.ndarray:
    delta = np.diff(close, prepend=close[0])
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(period).mean().values
    avg_loss = pd.Series(loss).rolling(period).mean().values
    rs = np.divide(avg_gain, avg_loss, out=np.zeros_like(avg_gain), where=avg_loss != 0)
    return 100 - (100 / (1 + rs))


def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    hl = high - low
    hc = np.abs(high - np.roll(close, 1))
    lc = np.abs(low - np.roll(close, 1))
    tr = np.maximum(hl, np.maximum(hc, lc))
    return pd.Series(tr).rolling(period).mean().values


def adx(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> tuple:
    up = high - np.roll(high, 1)
    down = np.roll(low, 1) - low
    plus_dm = np.where((up > down) & (up > 0), up, 0)
    minus_dm = np.where((down > up) & (down > 0), down, 0)
    tr_series = pd.Series(np.maximum(high - low, np.maximum(np.abs(high - np.roll(close, 1)), np.abs(low - np.roll(close, 1)))))
    atr_vals = tr_series.rolling(period).mean().values
    plus_di = 100 * pd.Series(plus_dm).rolling(period).mean().values / np.where(atr_vals != 0, atr_vals, 1)
    minus_di = 100 * pd.Series(minus_dm).rolling(period).mean().values / np.where(atr_vals != 0, atr_vals, 1)
    dx = 100 * np.abs(plus_di - minus_di) / np.where((plus_di + minus_di) != 0, plus_di + minus_di, 1)
    adx_vals = pd.Series(dx).rolling(period).mean().values
    return adx_vals, plus_di, minus_di


def stochastic(high: np.ndarray, low: np.ndarray, close: np.ndarray, k_period: int = 14) -> tuple:
    lowest_low = pd.Series(low).rolling(k_period).min().values
    highest_high = pd.Series(high).rolling(k_period).max().values
    k = 100 * (close - lowest_low) / np.where((highest_high - lowest_low) != 0, highest_high - lowest_low, 1)
    d = pd.Series(k).rolling(3).mean().values
    return k, d


def ichimoku(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> dict:
    tenkan = (pd.Series(high).rolling(9).max().values + pd.Series(low).rolling(9).min().values) / 2
    kijun = (pd.Series(high).rolling(26).max().values + pd.Series(low).rolling(26).min().values) / 2
    senkou_a = (tenkan + kijun) / 2
    senkou_b = (pd.Series(high).rolling(52).max().values + pd.Series(low).rolling(52).min().values) / 2
    chikou = np.roll(close, -26)
    return {
        "tenkan_sen": tenkan.tolist() if hasattr(tenkan, 'tolist') else tenkan,
        "kijun_sen": kijun.tolist() if hasattr(kijun, 'tolist') else kijun,
        "senkou_span_a": senkou_a.tolist() if hasattr(senkou_a, 'tolist') else senkou_a,
        "senkou_span_b": senkou_b.tolist() if hasattr(senkou_b, 'tolist') else senkou_b,
        "chikou_span": chikou.tolist() if hasattr(chikou, 'tolist') else chikou,
    }


def aroon(high: np.ndarray, low: np.ndarray, period: int = 25) -> tuple:
    aroon_up = np.full_like(high, np.nan)
    aroon_down = np.full_like(high, np.nan)
    for i in range(period - 1, len(high)):
        days_since_high = np.argmax(high[i - period + 1:i + 1][::-1]) if len(high[i - period + 1:i + 1]) > 0 else 0
        days_since_low = np.argmin(low[i - period + 1:i + 1][::-1]) if len(low[i - period + 1:i + 1]) > 0 else 0
        aroon_up[i] = ((period - days_since_high) / period) * 100
        aroon_down[i] = ((period - days_since_low) / period) * 100
    return aroon_up, aroon_down


def williams_r(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
    highest = pd.Series(high).rolling(period).max().values
    lowest = pd.Series(low).rolling(period).min().values
    return -100 * (highest - close) / np.where((highest - lowest) != 0, highest - lowest, 1)


def mfi(high: np.ndarray, low: np.ndarray, close: np.ndarray, volume: np.ndarray, period: int = 14) -> np.ndarray:
    typical = (high + low + close) / 3
    money_flow = typical * volume
    positive = np.where(typical > np.roll(typical, 1), money_flow, 0)
    negative = np.where(typical < np.roll(typical, 1), money_flow, 0)
    ratio = pd.Series(positive).rolling(period).sum().values / np.where(pd.Series(negative).rolling(period).sum().values != 0, pd.Series(negative).rolling(period).sum().values, 1)
    return 100 - (100 / (1 + ratio))


def cci(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 20) -> np.ndarray:
    tp = (high + low + close) / 3
    sma = pd.Series(tp).rolling(period).mean().values
    mad = pd.Series(tp).rolling(period).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True).values
    mad = np.where(mad == 0, 0.001, mad)
    return (tp - sma) / (0.015 * mad)


def roc(close: np.ndarray, period: int = 12) -> np.ndarray:
    return np.where(pd.Series(close).shift(period).values != 0, ((close - pd.Series(close).shift(period).values) / pd.Series(close).shift(period).values) * 100, 0)


def keltner(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 20, multiplier: float = 2.0) -> tuple:
    ema = pd.Series(close).ewm(span=period).mean().values
    atr_vals = atr(high, low, close, period)
    return ema + multiplier * atr_vals, ema, ema - multiplier * atr_vals


def demark(close: np.ndarray, period: int = 13) -> tuple:
    """Tom DeMark Sequential / TD Sequential setup."""
    setup_buy = np.full_like(close, 0)
    setup_sell = np.full_like(close, 0)
    for i in range(period, len(close)):
        if close[i] < close[i - period]:
            setup_buy[i] = setup_buy[i - 1] + 1 if i > 0 else 1
        else:
            setup_buy[i] = 0
        if close[i] > close[i - period]:
            setup_sell[i] = setup_sell[i - 1] + 1 if i > 0 else 1
        else:
            setup_sell[i] = 0
    return setup_buy, setup_sell


def detect_candlestick_patterns(df: pd.DataFrame) -> list:
    patterns = []
    if df.empty or len(df) < 2:
        return patterns
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    o, h, l, c = float(last["Open"]), float(last["High"]), float(last["Low"]), float(last["Close"])
    po, ph, pl, pc = float(prev["Open"]), float(prev["High"]), float(prev["Low"]), float(prev["Close"])
    body = abs(c - o)
    upper_wick = h - max(o, c)
    lower_wick = min(o, c) - l
    total_range = h - l

    if total_range == 0:
        return patterns

    bullish = c > o
    bearish = c < o

    # Doji
    if body / total_range < 0.1:
        patterns.append({"pattern": "Doji", "signal": "neutral", "detail": "Indecision — cat is ambivalent"})

    # Hammer
    if bullish and lower_wick >= 2 * body and upper_wick <= 0.3 * body:
        patterns.append({"pattern": "Hammer", "signal": "bullish", "detail": "Reversal up — the cat stamps its paw"})

    # Shooting Star
    if bearish and upper_wick >= 2 * body and lower_wick <= 0.3 * body:
        patterns.append({"pattern": "Shooting Star", "signal": "bearish", "detail": "Reversal down — cat hisses at the top"})

    # Engulfing
    if bullish and bearish and c > po and o < pc and abs(c - o) > abs(pc - po):
        patterns.append({"pattern": "Bullish Engulfing", "signal": "bullish", "detail": "Cats ate the bears"})
    if bearish and bullish and c < po and o > pc and abs(c - o) > abs(pc - po):
        patterns.append({"pattern": "Bearish Engulfing", "signal": "bearish", "detail": "Bears ate the cats"})

    # Morning Star (3-candle)
    if len(df) >= 3:
        prev2 = df.iloc[-3]
        p2c = float(prev2["Close"])
        p2o = float(prev2["Open"])
        if bearish and body > total_range * 0.6 and p2c < p2o and abs(p2c - p2o) > 0 and abs(pc - po) > 0:
            if (pc - po) / abs(pc - po) != (p2c - p2o) / abs(p2c - p2o):
                patterns.append({"pattern": "Morning Star", "signal": "bullish", "detail": "3-candle reversal — the cat wakes up"})

    if not patterns:
        patterns.append({"pattern": "None", "signal": "neutral", "detail": "No significant pattern detected"})
    return patterns


async def calculate_technicals(ticker: str, period: str = "1y") -> dict:
    records = await get_history(ticker, period)
    if not records:
        return {"ticker": ticker, "error": "No data"}
    df = _hist_to_df(records)
    if df.empty or len(df) < 30:
        return {"ticker": ticker, "error": "Insufficient data"}
    close = df["Close"].values
    high = df["High"].values
    low = df["Low"].values
    volume = df["Volume"].values if "Volume" in df.columns else np.ones_like(close)
    result = {"ticker": ticker, "latest_price": _clean(close[-1])}

    # SMA
    for p in [5, 10, 20, 50, 200]:
        if len(close) >= p:
            result[f"SMA_{p}"] = _clean(pd.Series(close).rolling(p).mean().values[-1])
            result[f"SMA_{p}_trend"] = "above" if close[-1] > result[f"SMA_{p}"] else "below"

    # EMA
    for p in [12, 26]:
        result[f"EMA_{p}"] = _clean(pd.Series(close).ewm(span=p).mean().values[-1])

    # MACD
    macd = pd.Series(close).ewm(span=12).mean() - pd.Series(close).ewm(span=26).mean()
    signal = macd.ewm(span=9).mean()
    result["MACD"] = _clean(macd.values[-1])
    result["MACD_Signal"] = _clean(signal.values[-1])
    result["MACD_Hist"] = _clean((macd.values[-1] - signal.values[-1]))
    result["MACD_Crossover"] = "bullish" if result["MACD"] > result["MACD_Signal"] else "bearish"

    # RSI
    rsi_vals = rsi(close)
    result["RSI_14"] = _clean(rsi_vals[-1])
    if result["RSI_14"] is not None:
        if result["RSI_14"] > 70:
            result["RSI_Signal"] = "overbought 🟡"
        elif result["RSI_14"] < 30:
            result["RSI_Signal"] = "oversold 🟢"
        else:
            result["RSI_Signal"] = "neutral"

    # Bollinger Bands
    sma20 = pd.Series(close).rolling(20).mean().values
    std20 = pd.Series(close).rolling(20).std().values
    result["BB_Upper"] = _clean(sma20[-1] + 2 * std20[-1])
    result["BB_Middle"] = _clean(sma20[-1])
    result["BB_Lower"] = _clean(sma20[-1] - 2 * std20[-1])
    if result["BB_Upper"] and result["BB_Lower"]:
        if close[-1] > result["BB_Upper"]:
            result["BB_Signal"] = "above upper 🔴"
        elif close[-1] < result["BB_Lower"]:
            result["BB_Signal"] = "below lower 🟢"
        else:
            result["BB_Signal"] = "within bands"

    # ATR
    atr_vals = atr(high, low, close)
    result["ATR_14"] = _clean(atr_vals[-1])

    # OBV
    obv = (np.sign(np.diff(close, prepend=close[0])) * volume).cumsum()
    result["OBV"] = _clean(obv[-1])

    # ADX
    adx_vals, plus_di, minus_di = adx(high, low, close)
    result["ADX_14"] = _clean(adx_vals[-1])
    result["DI_Plus"] = _clean(plus_di[-1])
    result["DI_Minus"] = _clean(minus_di[-1])
    if result["ADX_14"] is not None:
        if result["ADX_14"] > 25:
            result["ADX_Trend"] = "strong trend"
        else:
            result["ADX_Trend"] = "weak/range"

    # Stochastic
    stoch_k, stoch_d = stochastic(high, low, close)
    result["Stoch_K"] = _clean(stoch_k[-1])
    result["Stoch_D"] = _clean(stoch_d[-1])

    # Williams %R
    wr = williams_r(high, low, close)
    result["Williams_%R"] = _clean(wr[-1])

    # MFI
    mfi_vals = mfi(high, low, close, volume)
    result["MFI_14"] = _clean(mfi_vals[-1])

    # CCI
    cci_vals = cci(high, low, close)
    result["CCI_20"] = _clean(cci_vals[-1])
    if result["CCI_20"] is not None:
        if result["CCI_20"] > 100:
            result["CCI_Signal"] = "overbought"
        elif result["CCI_20"] < -100:
            result["CCI_Signal"] = "oversold"
        else:
            result["CCI_Signal"] = "neutral"

    # Aroon
    ar_up, ar_down = aroon(high, low)
    result["Aroon_Up"] = _clean(ar_up[-1])
    result["Aroon_Down"] = _clean(ar_down[-1])

    # ROC
    roc_vals = roc(close)
    result["ROC_12"] = _clean(roc_vals[-1])

    # Keltner Channels
    kelt_upper, kelt_mid, kelt_lower = keltner(high, low, close)
    result["Keltner_Upper"] = _clean(kelt_upper[-1])
    result["Keltner_Middle"] = _clean(kelt_mid[-1])
    result["Keltner_Lower"] = _clean(kelt_lower[-1])

    # DeMark Sequential
    demark_buy, demark_sell = demark(close)
    result["DeMark_Buy_Setup"] = _clean(demark_buy[-1])
    result["DeMark_Sell_Setup"] = _clean(demark_sell[-1])

    # Candlestick patterns
    result["patterns"] = detect_candlestick_patterns(df)

    # Overall signal
    bullish_signals = 0
    bearish_signals = 0
    for p in result["patterns"]:
        if p["signal"] == "bullish":
            bullish_signals += 1
        elif p["signal"] == "bearish":
            bearish_signals += 1
    if bullish_signals > bearish_signals:
        result["overall_signal"] = "BULLISH 🐱📈"
        result["confidence"] = min(100, 50 + (bullish_signals - bearish_signals) * 15)
    elif bearish_signals > bullish_signals:
        result["overall_signal"] = "BEARISH 🐱📉"
        result["confidence"] = min(100, 50 + (bearish_signals - bullish_signals) * 15)
    else:
        result["overall_signal"] = "NEUTRAL 🐱"
        result["confidence"] = 50

    result["cat_commentary"] = random_cat_commentary(result.get("RSI_14", 50), result.get("overall_signal", "NEUTRAL"))
    return result


def random_cat_commentary(rsi_val: float = 50, signal: str = "NEUTRAL") -> str:
    import random
    comments = [
        "The cat has reviewed the charts. The whiskers say: {signal}",
        "After careful paw-lysis, Miau AI recommends {signal}",
        "The cat stared at this chart for 9 lives. Verdict: {signal}",
        "This analysis was purr-reviewed by the feline committee. Result: {signal}",
        "The catnip indicator is flashing {signal}",
    ]
    return random.choice(comments).format(signal=signal.lower())


async def generate_signals_summary(ticker: str, period: str = "1y") -> dict:
    ta = await calculate_technicals(ticker, period)
    if "error" in ta:
        return ta
    signals = []
    price = ta["latest_price"]
    # RSI
    if ta.get("RSI_14") is not None:
        if ta["RSI_14"] < 30:
            signals.append({"type": "BUY", "indicator": "RSI", "detail": f"Oversold ({ta['RSI_14']:.0f})", "strength": "strong"})
        elif ta["RSI_14"] > 70:
            signals.append({"type": "SELL", "indicator": "RSI", "detail": f"Overbought ({ta['RSI_14']:.0f})", "strength": "strong"})
    # MACD
    if ta.get("MACD_Crossover") == "bullish":
        signals.append({"type": "BUY", "indicator": "MACD", "detail": "MACD above signal line", "strength": "moderate"})
    elif ta.get("MACD_Crossover") == "bearish":
        signals.append({"type": "SELL", "indicator": "MACD", "detail": "MACD below signal line", "strength": "moderate"})
    # SMA trend
    for p in [20, 50, 200]:
        if ta.get(f"SMA_{p}_trend") == "above":
            signals.append({"type": "BUY", "indicator": f"SMA_{p}", "detail": f"Price above SMA{p}", "strength": "weak"})
        elif ta.get(f"SMA_{p}_trend") == "below":
            signals.append({"type": "SELL", "indicator": f"SMA_{p}", "detail": f"Price below SMA{p}", "strength": "weak"})
    # Bollinger
    if ta.get("BB_Signal") == "below lower 🟢":
        signals.append({"type": "BUY", "indicator": "Bollinger", "detail": "Price below lower band", "strength": "moderate"})
    elif ta.get("BB_Signal") == "above upper 🔴":
        signals.append({"type": "SELL", "indicator": "Bollinger", "detail": "Price above upper band", "strength": "moderate"})
    return {
        "ticker": ticker,
        "price": price,
        "signals": signals,
        "signal_count": len(signals),
        "overall_signal": ta.get("overall_signal", "NEUTRAL"),
        "confidence": ta.get("confidence", 50),
        "cat_commentary": ta.get("cat_commentary", ""),
    }
