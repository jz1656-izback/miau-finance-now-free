from fastapi import APIRouter, Query
from typing import Optional
from app.services.analytics import risk as risk_service

router = APIRouter()


@router.get("/var")
async def value_at_risk(ticker: str = "SPY", confidence: float = 0.95, method: str = "historical", period: str = "2y"):
    return await risk_service.calculate_var(ticker, confidence, method, period)


@router.get("/beta")
async def beta(ticker: str = "AAPL", benchmark: str = "SPY", period: str = "2y"):
    return await risk_service.calculate_beta(ticker, benchmark, period)


@router.get("/stress-test")
async def stress_test(ticker: str = "SPY", period: str = "2y"):
    return await risk_service.stress_test_scenarios(ticker, period)


@router.get("/greeks")
async def greeks(spot: float = 100, strike: float = 105, days_to_expiry: float = 30,
                  risk_free: float = 0.05, volatility: float = 0.25, option_type: str = "call"):
    return risk_service.greeks_calc(spot, strike, days_to_expiry / 365, risk_free, volatility, option_type)


@router.get("/comprehensive")
async def comprehensive_risk(ticker: str = "AAPL", period: str = "2y"):
    return await risk_service.comprehensive_risk(ticker, period)


@router.get("/rolling")
async def rolling_metrics(
    ticker: str = "AAPL",
    benchmark: str = "SPY",
    window: str = "12mo",
    period: str = "3y",
):
    return await risk_service.rolling_risk(ticker, benchmark, window, period)
