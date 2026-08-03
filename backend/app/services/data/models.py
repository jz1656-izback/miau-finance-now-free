"""Typed Pydantic models for all data source responses."""
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


# ── Health ─────────────────────────────────────────────────────

class HealthStatus(BaseModel):
    provider: str
    healthy: bool
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    last_success: Optional[datetime] = None


# ── Market Data ────────────────────────────────────────────────

class Quote(BaseModel):
    ticker: str
    price: float
    change: float
    change_pct: float
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[int] = None
    previous_close: Optional[float] = None
    timestamp: datetime


class OHLCV(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class Fundamentals(BaseModel):
    ticker: str
    company_name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    eps: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    revenue: Optional[float] = None
    revenue_growth: Optional[float] = None
    profit_margin: Optional[float] = None
    debt_to_equity: Optional[float] = None
    free_cash_flow: Optional[float] = None
    target_price: Optional[float] = None
    recommendation: Optional[str] = None


# ── Quant / Alternative ────────────────────────────────────────

class QuantHealthScore(BaseModel):
    ticker: str
    piotroski_f_score: Optional[int] = None
    altman_z_score: Optional[float] = None
    beneish_m_score: Optional[float] = None
    roic_wacc_spread: Optional[float] = None


class FairValue(BaseModel):
    ticker: str
    fair_price: Optional[float] = None
    current_price: Optional[float] = None
    upside_pct: Optional[float] = None
    wacc: Optional[float] = None
    sensitivity_matrix: Optional[list[list[float]]] = None


class InsiderTrade(BaseModel):
    ticker: str
    name: str
    relationship: str
    transaction_type: str
    shares: int
    price: float
    value: float
    date: datetime


# ── DeFi ───────────────────────────────────────────────────────

class DefiProtocol(BaseModel):
    name: str
    chain: str
    tvl: float
    category: str
    change_24h: Optional[float] = None


class YieldPool(BaseModel):
    pool: str
    chain: str
    project: str
    apy: float
    tvl: float
    reward_tokens: Optional[list[str]] = None


class GasPrices(BaseModel):
    chain: str
    safe_gwei: float
    propose_gwei: float
    fast_gwei: float
    base_fee: Optional[float] = None
    estimated_usd: Optional[dict[str, float]] = None


# ── FX / Macro ─────────────────────────────────────────────────

class FXRate(BaseModel):
    base: str
    target: str
    rate: float
    date: str


class MacroIndicator(BaseModel):
    country: str
    indicator: str
    value: float
    change_yoy: Optional[float] = None
    date: str


# ── General Purpose ────────────────────────────────────────────

class DataSourceResponse(BaseModel):
    provider: str
    data: Any
    cached: bool = False
    latency_ms: float = 0
