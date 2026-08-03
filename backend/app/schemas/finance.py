from pydantic import BaseModel, field_validator
from typing import Optional, Any
from uuid import UUID
from datetime import datetime, date
from app.schemas.validators import safe_string_validator


def validate_ticker(v: str) -> str:
    from app.schemas.validators import TICKER_PATTERN
    if not TICKER_PATTERN.match(v.upper()):
        raise ValueError('Invalid ticker')
    return v.upper()


def positive_float_validator(v: float) -> float:
    if v <= 0:
        raise ValueError('Must be positive')
    return v


def non_negative_float_validator(v: float) -> float:
    if v < 0:
        raise ValueError('Must be non-negative')
    return v


class InstrumentCreate(BaseModel):
    ticker: str
    isin: Optional[str] = None
    sedol: Optional[str] = None
    cusip: Optional[str] = None
    name: str
    instrument_type: str
    currency: str = "USD"
    exchange: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    issue_date: Optional[date] = None
    maturity_date: Optional[date] = None
    coupon_rate: Optional[float] = None
    underlying_instrument_id: Optional[UUID] = None
    strike_price: Optional[float] = None
    option_type: Optional[str] = None
    metadata: dict = {}

    _validate_ticker = field_validator("ticker")(validate_ticker)
    _validate_name = field_validator("name")(safe_string_validator)
    _validate_instrument_type = field_validator("instrument_type")(safe_string_validator)
    _validate_exchange = field_validator("exchange")(safe_string_validator)
    _validate_sector = field_validator("sector")(safe_string_validator)


class Instrument(InstrumentCreate):
    id: UUID
    ontology_object_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PortfolioCreate(BaseModel):
    name: str
    portfolio_type: str = "trading"
    base_currency: str = "USD"
    management_style: Optional[str] = None
    benchmark_id: Optional[str] = None
    metadata: dict = {}

    _validate_name = field_validator("name")(safe_string_validator)
    _validate_portfolio_type = field_validator("portfolio_type")(safe_string_validator)
    _validate_management_style = field_validator("management_style")(safe_string_validator)


class Portfolio(PortfolioCreate):
    id: UUID
    ontology_object_id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class TradeCreate(BaseModel):
    trade_id: Optional[str] = None
    instrument_id: UUID
    portfolio_id: Optional[UUID] = None
    counterparty_id: Optional[UUID] = None
    trade_date: datetime = datetime.now()
    settlement_date: Optional[datetime] = None
    trade_type: str
    side: str
    quantity: float
    price: float
    notional: Optional[float] = None
    commission: float = 0
    fees: float = 0
    currency: str = "USD"
    trader: Optional[str] = None
    broker: Optional[str] = None
    metadata: dict = {}

    _validate_trade_type = field_validator("trade_type")(safe_string_validator)
    _validate_side = field_validator("side")(safe_string_validator)
    _validate_currency = field_validator("currency")(safe_string_validator)
    _validate_trader = field_validator("trader")(safe_string_validator)
    _validate_broker = field_validator("broker")(safe_string_validator)
    _validate_quantity = field_validator("quantity")(positive_float_validator)
    _validate_price = field_validator("price")(non_negative_float_validator)


class Trade(TradeCreate):
    id: UUID
    ontology_object_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PnLRow(BaseModel):
    portfolio_id: UUID
    instrument_id: Optional[UUID] = None
    pnl_type: str
    pnl_amount: float
    currency: str = "USD"
    source: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    attribution: dict = {}


class RiskMetric(BaseModel):
    portfolio_id: UUID
    instrument_id: Optional[UUID] = None
    metric_name: str
    metric_value: float
    metric_type: Optional[str] = None
    currency: str = "USD"
    parameters: dict = {}
