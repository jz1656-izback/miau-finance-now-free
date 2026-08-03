import hashlib
import os
import joblib
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor

from app.cache_utils import cached

MODEL_DIR = os.getenv("EARNINGS_MODEL_DIR", "/app/models/earnings")


@cached(ttl=86400, prefix="earnings")
async def fetch_earnings(ticker: str) -> list[dict]:
    stock = yf.Ticker(ticker)
    earnings = stock.earnings
    if earnings is None or earnings.empty:
        return []
    earnings = earnings.reset_index()
    result = []
    for _, row in earnings.iterrows():
        result.append({
            "date": str(row.get("index", row.get("Date", row.name))),
            "eps_actual": float(row.get("eps_actual", row.get("EPS Actual", 0))),
            "eps_estimate": float(row.get("eps_estimate", row.get("EPS Estimate", 0))),
            "revenue_actual": float(row.get("revenue_actual", row.get("Revenue Actual", 0))),
            "revenue_estimate": float(row.get("revenue_estimate", row.get("Revenue Estimate", 0))),
            "surprise_pct": float(
                row.get("surprise_pct", row.get("Surprise(%)", 0))
            ),
        })
    return result


async def build_features(ticker: str) -> pd.DataFrame:
    raw = await fetch_earnings(ticker)
    if not raw:
        return pd.DataFrame()

    df = pd.DataFrame(raw)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    df["surprise_pct_rolling_avg"] = df["surprise_pct"].rolling(window=4, min_periods=1).mean()
    df["eps_growth_rate"] = df["eps_actual"].pct_change()
    df["revenue_growth_rate"] = df["revenue_actual"].pct_change()
    df["days_since_last_earnings"] = df["date"].diff().dt.days.fillna(0)

    df = df.dropna(subset=["surprise_pct_rolling_avg"])
    return df


async def train_model(ticker: str) -> RandomForestRegressor:
    df = await build_features(ticker)
    if df.empty or len(df) < 5:
        raise ValueError(f"Not enough earnings data for {ticker}")

    feature_cols = ["surprise_pct_rolling_avg", "eps_growth_rate", "revenue_growth_rate", "days_since_last_earnings"]
    existing_cols = [c for c in feature_cols if c in df.columns]
    X = df[existing_cols].fillna(0)
    y = df["surprise_pct"].fillna(0)

    model = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X, y)
    return model


def save_model(model, ticker: str) -> str:
    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, f"{ticker}.joblib")
    joblib.dump(model, path)
    integrity_path = path + ".sha256"
    with open(integrity_path, "w") as f:
        f.write(hashlib.sha256(open(path, "rb").read()).hexdigest())
    return path


def load_model(ticker: str) -> Optional[RandomForestRegressor]:
    path = os.path.join(MODEL_DIR, f"{ticker}.joblib")
    if not os.path.exists(path):
        return None
    integrity_path = path + ".sha256"
    if os.path.exists(integrity_path):
        stored_hash = open(integrity_path).read().strip()
        current_hash = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if stored_hash != current_hash:
            return None
    return joblib.load(path)


def model_age(path: str) -> Optional[timedelta]:
    if not os.path.exists(path):
        return None
    mtime = datetime.fromtimestamp(os.path.getmtime(path))
    return datetime.now() - mtime


async def get_or_train_model(ticker: str) -> RandomForestRegressor:
    path = os.path.join(MODEL_DIR, f"{ticker}.pkl")
    age = model_age(path)
    if age is None or age > timedelta(days=7):
        model = await train_model(ticker)
        save_model(model, ticker)
    else:
        model = load_model(ticker)
        if model is None:
            model = await train_model(ticker)
            save_model(model, ticker)
    return model


async def predict_earnings(ticker: str) -> dict:
    model = await get_or_train_model(ticker)
    df = await build_features(ticker)
    if df.empty:
        return {"ticker": ticker, "error": "No earnings data available"}

    feature_cols = ["surprise_pct_rolling_avg", "eps_growth_rate", "revenue_growth_rate", "days_since_last_earnings"]
    existing_cols = [c for c in feature_cols if c in df.columns]
    latest = df[existing_cols].iloc[-1:].fillna(0)
    prediction = float(model.predict(latest)[0])

    return {
        "ticker": ticker,
        "predicted_surprise_pct": round(prediction, 4),
        "last_actual_surprise_pct": float(df["surprise_pct"].iloc[-1]),
        "last_eps_actual": float(df["eps_actual"].iloc[-1]),
        "last_revenue_actual": float(df["revenue_actual"].iloc[-1]),
        "data_points": len(df),
    }
