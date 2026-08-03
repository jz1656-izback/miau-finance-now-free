from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


ISO_CURRENCIES = {
    "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound", "JPY": "Japanese Yen",
    "CHF": "Swiss Franc", "CAD": "Canadian Dollar", "AUD": "Australian Dollar",
    "NZD": "New Zealand Dollar", "CNY": "Chinese Yuan", "HKD": "Hong Kong Dollar",
    "SGD": "Singapore Dollar", "SEK": "Swedish Krona", "NOK": "Norwegian Krone",
    "KRW": "South Korean Won", "INR": "Indian Rupee", "BRL": "Brazilian Real",
    "MXN": "Mexican Peso", "ZAR": "South African Rand", "TRY": "Turkish Lira",
    "RUB": "Russian Ruble", "PLN": "Polish Zloty", "DKK": "Danish Krone",
    "THB": "Thai Baht", "IDR": "Indonesian Rupiah", "MYR": "Malaysian Ringgit",
    "PHP": "Philippine Peso", "TWD": "Taiwan Dollar", "AED": "UAE Dirham",
    "SAR": "Saudi Riyal", "ILS": "Israeli Shekel", "CLP": "Chilean Peso",
    "COP": "Colombian Peso", "PEN": "Peruvian Sol", "ARS": "Argentine Peso",
    "NGN": "Nigerian Naira", "KES": "Kenyan Shilling",
    "BTC": "Bitcoin", "ETH": "Ethereum", "SOL": "Solana", "XRP": "Ripple",
}

SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "CHF": "Fr",
    "CAD": "C$", "AUD": "A$", "NZD": "NZ$", "CNY": "¥", "HKD": "HK$",
    "SGD": "S$", "SEK": "kr", "NOK": "kr", "KRW": "₩", "INR": "₹",
    "BRL": "R$", "MXN": "Mex$", "ZAR": "R", "TRY": "₺", "RUB": "₽",
    "PLN": "zł", "DKK": "kr", "THB": "฿", "IDR": "Rp", "MYR": "RM",
    "PHP": "₱", "TWD": "NT$", "AED": "د.إ", "SAR": "﷼", "ILS": "₪",
    "CLP": "$", "COP": "$", "PEN": "S/", "ARS": "$", "NGN": "₦",
    "KES": "KSh", "BTC": "₿", "ETH": "Ξ", "SOL": "◎", "XRP": "✕",
}

DECIMAL_PLACES: dict[str, int] = {
    "JPY": 0, "KRW": 0, "IDR": 0, "CLP": 0, "COP": 0,
    "BTC": 8, "ETH": 8, "SOL": 4, "XRP": 6,
}


def validate_currency_code(v: str) -> str:
    code = v.upper()
    if code not in ISO_CURRENCIES:
        raise ValueError(f"Unsupported currency code: {code}")
    return code


class CurrencyResponse(BaseModel):
    code: str
    symbol: str
    name: str
    decimal_places: int = 2
    fx_rate: float = 1.0
    fx_updated_at: Optional[datetime] = None
    is_crypto: bool = False
    is_active: bool = True

    class Config:
        from_attributes = True


class ConversionRequest(BaseModel):
    from_currency: str = "USD"
    to_currency: str = "EUR"
    amount: float = 1.0

    _validate_from = field_validator("from_currency")(validate_currency_code)
    _validate_to = field_validator("to_currency")(validate_currency_code)


class ConversionResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
    rate: float
    inverse_rate: float
    timestamp: datetime
