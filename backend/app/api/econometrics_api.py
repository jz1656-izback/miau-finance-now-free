"""Econometrics & Quant API — OLS, Granger, Cointegration, CAPM, Risk, Correlation."""
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.middleware.auth import get_current_user
from app.services.analytics.econometrics import (
    ols_regression, granger_causality, cointegration_test,
    capm_analysis, correlation_matrix, risk_analysis,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/econometrics", tags=["Econometrics & Quant"])


@router.get("/ols")
async def ols(
    y: str = Query(..., description="Dependent variable ticker"),
    x: str = Query(..., description="Independent variable ticker"),
    period: str = Query("1y"),
    user: dict = Depends(get_current_user),
):
    result = await ols_regression(y.upper(), x.upper(), period)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@router.get("/granger")
async def granger(
    y: str = Query(..., description="Y variable (endogenous)"),
    x: str = Query(..., description="X variable (exogenous)"),
    max_lag: int = Query(5, le=10),
    period: str = Query("1y"),
    user: dict = Depends(get_current_user),
):
    result = await granger_causality(y.upper(), x.upper(), max_lag, period)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@router.get("/coint")
async def coint(
    a: str = Query(..., description="First ticker"),
    b: str = Query(..., description="Second ticker"),
    period: str = Query("2y"),
    user: dict = Depends(get_current_user),
):
    result = await cointegration_test(a.upper(), b.upper(), period)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@router.get("/capm")
async def capm(
    ticker: str = Query(...),
    benchmark: str = Query("SPY"),
    period: str = Query("2y"),
    risk_free_rate: float = Query(0.05),
    user: dict = Depends(get_current_user),
):
    result = await capm_analysis(ticker.upper(), benchmark.upper(), period, risk_free_rate)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@router.get("/risk")
async def risk(
    ticker: str = Query(...),
    period: str = Query("2y"),
    confidence: float = Query(0.95, ge=0.9, le=0.99),
    user: dict = Depends(get_current_user),
):
    result = await risk_analysis(ticker.upper(), period, confidence)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


@router.get("/correl")
async def correl(
    tickers: str = Query(..., description="Comma-separated tickers (e.g. AAPL,MSFT,GOOGL)"),
    period: str = Query("1y"),
    user: dict = Depends(get_current_user),
):
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if len(ticker_list) < 2:
        raise HTTPException(400, "Need at least 2 tickers")
    result = await correlation_matrix(ticker_list, period)
    if "error" in result:
        raise HTTPException(400, result["error"])
    return result
