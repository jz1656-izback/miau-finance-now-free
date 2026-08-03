import logging
from decimal import Decimal
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

SUPPORTED_CURRENCIES: dict[str, dict] = {
    "USD": {"symbol": "$", "name": "US Dollar", "decimals": 2, "crypto": False},
    "EUR": {"symbol": "€", "name": "Euro", "decimals": 2, "crypto": False},
    "GBP": {"symbol": "£", "name": "British Pound", "decimals": 2, "crypto": False},
    "JPY": {"symbol": "¥", "name": "Japanese Yen", "decimals": 0, "crypto": False},
    "CHF": {"symbol": "CHF", "name": "Swiss Franc", "decimals": 2, "crypto": False},
    "CAD": {"symbol": "C$", "name": "Canadian Dollar", "decimals": 2, "crypto": False},
    "AUD": {"symbol": "A$", "name": "Australian Dollar", "decimals": 2, "crypto": False},
    "CNY": {"symbol": "¥", "name": "Chinese Yuan", "decimals": 2, "crypto": False},
    "HKD": {"symbol": "HK$", "name": "Hong Kong Dollar", "decimals": 2, "crypto": False},
    "SGD": {"symbol": "S$", "name": "Singapore Dollar", "decimals": 2, "crypto": False},
    "INR": {"symbol": "₹", "name": "Indian Rupee", "decimals": 2, "crypto": False},
    "MXN": {"symbol": "Mex$", "name": "Mexican Peso", "decimals": 2, "crypto": False},
    "BRL": {"symbol": "R$", "name": "Brazilian Real", "decimals": 2, "crypto": False},
    "ZAR": {"symbol": "R", "name": "South African Rand", "decimals": 2, "crypto": False},
    "SEK": {"symbol": "kr", "name": "Swedish Krona", "decimals": 2, "crypto": False},
    "NOK": {"symbol": "kr", "name": "Norwegian Krone", "decimals": 2, "crypto": False},
    "KRW": {"symbol": "₩", "name": "South Korean Won", "decimals": 0, "crypto": False},
    "BTC": {"symbol": "₿", "name": "Bitcoin", "decimals": 8, "crypto": True},
    "ETH": {"symbol": "Ξ", "name": "Ethereum", "decimals": 8, "crypto": True},
    "USDT": {"symbol": "₮", "name": "Tether", "decimals": 2, "crypto": True},
}


async def get_fx_rate(db: AsyncSession, from_currency: str, to_currency: str) -> Optional[Decimal]:
    if from_currency == to_currency:
        return Decimal("1.0")
    result = await db.execute(
        text("""
            SELECT
                c_from.fx_rate / c_to.fx_rate as rate
            FROM currencies c_from, currencies c_to
            WHERE c_from.code = :from_code AND c_to.code = :to_code
              AND c_from.is_active AND c_to.is_active
        """),
        {"from_code": from_currency, "to_code": to_currency},
    )
    row = result.mappings().first()
    if not row:
        return None
    return Decimal(str(row["rate"]))


async def convert_amount(
    db: AsyncSession,
    amount: Decimal,
    from_currency: str,
    to_currency: str,
) -> Optional[Decimal]:
    rate = await get_fx_rate(db, from_currency, to_currency)
    if rate is None:
        return None
    converted = amount * rate
    info = SUPPORTED_CURRENCIES.get(to_currency, SUPPORTED_CURRENCIES["USD"])
    return round(converted, info["decimals"])


async def list_currencies(db: AsyncSession) -> list[dict]:
    result = await db.execute(
        text("""
            SELECT code, symbol, name, decimal_places, fx_rate, fx_updated_at, is_crypto, is_active
            FROM currencies
            WHERE is_active = TRUE
            ORDER BY is_crypto ASC, code ASC
        """)
    )
    return [dict(r) for r in result.mappings().all()]


async def get_currency_info(code: str) -> Optional[dict]:
    info = SUPPORTED_CURRENCIES.get(code.upper())
    if not info:
        return None
    return {"code": code.upper(), **info}


async def update_portfolio_currency(
    db: AsyncSession,
    portfolio_id: str,
    new_currency: str,
    user_id: str,
) -> Optional[dict]:
    portfolio = await db.execute(
        text("SELECT id, base_currency FROM portfolios WHERE id = :id"),
        {"id": portfolio_id},
    )
    row = portfolio.mappings().first()
    if not row:
        return None

    old_currency = row["base_currency"] or "USD"
    if old_currency == new_currency:
        return {"id": str(row["id"]), "base_currency": new_currency, "converted": False}

    rate = await get_fx_rate(db, old_currency, new_currency)
    if rate is None:
        return None

    await db.execute(
        text("UPDATE portfolios SET base_currency = :currency WHERE id = :id"),
        {"currency": new_currency, "id": portfolio_id},
    )

    positions = await db.execute(
        text("""
            UPDATE positions
            SET market_value = market_value * :rate,
                cost_basis = cost_basis * :rate,
                unrealized_pnl = unrealized_pnl * :rate,
                realized_pnl = realized_pnl * :rate,
                currency = :currency
            WHERE portfolio_id = :pid
            RETURNING id
        """),
        {"rate": rate, "currency": new_currency, "pid": portfolio_id},
    )
    await db.commit()
    pos_count = len(positions.mappings().all())
    return {
        "id": str(row["id"]),
        "old_currency": old_currency,
        "base_currency": new_currency,
        "rate": float(rate),
        "positions_converted": pos_count,
        "converted": True,
    }
