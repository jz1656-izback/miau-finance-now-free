import logging
from typing import Optional
from datetime import datetime

from app.cache import get_cache, set_cache

logger = logging.getLogger(__name__)

MAJOR_PAIRS = {
    "EUR": "EURUSD=X", "GBP": "GBPUSD=X", "JPY": "USDJPY=X",
    "CHF": "USDCHF=X", "CAD": "USDCAD=X", "AUD": "AUDUSD=X",
    "NZD": "NZDUSD=X", "CNY": "USDCNY=X", "INR": "USDINR=X",
    "BRL": "USDBRL=X", "KRW": "USDKRW=X", "SEK": "USDSEK=X",
    "NOK": "USDNOK=X", "MXN": "USDMXN=X", "SGD": "USDSGD=X",
    "HKD": "USDHKD=X", "TRY": "USDTRY=X", "ZAR": "USDZAR=X",
    "PLN": "USDPLN=X", "DKK": "USDDKK=X",
}

CURRENCY_META = {
    "USD": {"symbol": "$",  "decimals": 2, "name": "US Dollar"},
    "EUR": {"symbol": "\u20ac",  "decimals": 2, "name": "Euro"},
    "GBP": {"symbol": "\u00a3",  "decimals": 2, "name": "British Pound"},
    "JPY": {"symbol": "\u00a5",  "decimals": 0, "name": "Japanese Yen"},
    "CHF": {"symbol": "Fr", "decimals": 2, "name": "Swiss Franc"},
    "CAD": {"symbol": "C$", "decimals": 2, "name": "Canadian Dollar"},
    "AUD": {"symbol": "A$", "decimals": 2, "name": "Australian Dollar"},
    "NZD": {"symbol": "NZ$","decimals": 2, "name": "New Zealand Dollar"},
    "CNY": {"symbol": "\u5143",  "decimals": 2, "name": "Chinese Yuan"},
    "INR": {"symbol": "\u20b9",  "decimals": 2, "name": "Indian Rupee"},
    "BRL": {"symbol": "R$", "decimals": 2, "name": "Brazilian Real"},
    "KRW": {"symbol": "\u20a9",  "decimals": 0, "name": "South Korean Won"},
    "SEK": {"symbol": "kr", "decimals": 2, "name": "Swedish Krona"},
    "NOK": {"symbol": "kr", "decimals": 2, "name": "Norwegian Krone"},
    "MXN": {"symbol": "Mex$","decimals":2, "name": "Mexican Peso"},
    "SGD": {"symbol": "S$",  "decimals": 2, "name": "Singapore Dollar"},
    "HKD": {"symbol": "HK$", "decimals": 2, "name": "Hong Kong Dollar"},
    "TRY": {"symbol": "\u20ba",  "decimals": 2, "name": "Turkish Lira"},
    "ZAR": {"symbol": "R",   "decimals": 2, "name": "South African Rand"},
    "PLN": {"symbol": "z\u0142",  "decimals": 2, "name": "Polish Zloty"},
    "DKK": {"symbol": "kr",  "decimals": 2, "name": "Danish Krone"},
}

CACHE_KEY = "forex:rates"
CACHE_TTL = 60

_rates_cache: dict[str, float] = {}
_last_fetch: Optional[datetime] = None


async def get_fx_rates(force_refresh: bool = False) -> dict[str, float]:
    global _rates_cache, _last_fetch
    now = datetime.now()

    if not force_refresh:
        cached = await get_cache(CACHE_KEY)
        if cached is not None:
            _rates_cache = cached
            _last_fetch = now
            return cached
        if _last_fetch and (now - _last_fetch).seconds < CACHE_TTL:
            return _rates_cache

    rates: dict[str, float] = {"USD": 1.0}
    try:
        import yfinance as yf
        pairs = list(MAJOR_PAIRS.values())
        data = yf.download(pairs, period="1d", progress=False)
        if data is not None and not data.empty:
            close = data["Close"] if "Close" in data else data.get("Adj Close", data)
            for code, yahoo_ticker in MAJOR_PAIRS.items():
                if yahoo_ticker in close.columns:
                    raw = float(close[yahoo_ticker].dropna().iloc[-1])
                    if yahoo_ticker.startswith("USD"):
                        rates[code] = 1.0 / raw if raw != 0 else 0
                    else:
                        rates[code] = raw
        _rates_cache = rates
        _last_fetch = now
        await set_cache(CACHE_KEY, rates, ttl=CACHE_TTL)
    except Exception as e:
        logger.warning("Failed to fetch FX rates: %s", e)
        if not _rates_cache:
            for code in MAJOR_PAIRS:
                rates[code] = 1.0
            _rates_cache = rates
    return rates


async def get_rate_history(pair_code: str, period: str = "1mo") -> list[dict]:
    yahoo_ticker = MAJOR_PAIRS.get(pair_code.upper())
    if not yahoo_ticker:
        return []
    try:
        import yfinance as yf
        t = yf.Ticker(yahoo_ticker)
        hist = t.history(period=period)
        if hist.empty:
            return []
        return [
            {"date": str(d.date()), "close": float(row["Close"]),
             "high": float(row["High"]), "low": float(row["Low"])}
            for d, row in hist.iterrows()
        ]
    except Exception as e:
        logger.warning("Failed to fetch rate history for %s: %s", pair_code, e)
        return []


async def convert(amount: float, from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return amount
    rates = await get_fx_rates()
    from_rate = rates.get(from_currency.upper(), 1.0)
    to_rate = rates.get(to_currency.upper(), 1.0)
    if from_rate == 0:
        return amount
    return round(amount * (1.0 / from_rate) * to_rate, 2)


async def format_currency(amount: float, currency: str) -> str:
    meta = CURRENCY_META.get(currency.upper(), {"symbol": "$", "decimals": 2})
    symbol = meta["symbol"]
    decimals = meta["decimals"]
    formatted = f"{amount:,.{decimals}f}"
    if currency.upper() == "USD":
        return f"${formatted}"
    return f"{formatted} {currency.upper()}"
