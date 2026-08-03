import logging
import os
from fastapi import FastAPI, Depends

# 🔇 Suppress yfinance HTTP error spam for fake tickers from static map data
logging.getLogger('yfinance').setLevel(logging.CRITICAL)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import ontology, instruments, portfolios, trades, search, pipelines, alerts, watchlist as watchlist_api
from app.middleware.metrics import PrometheusMiddleware
from app.api import ws as ws_api
from app.api import data_quality as data_quality_api
from app.api.analytics import (
    market as market_api, optimizer as optimizer_api, risk as risk_api,
    signals as signals_api, reports as reports_api, combined as analytics_api,
    news as news_api, fundamentals as fundamentals_api,
    economics as economics_api, fred as fred_api, options as options_api,
    monte_carlo as monte_carlo_api, sentiment as sentiment_api,
    factors as factors_api, attribution as attribution_api,
    regime as regime_api,
    pairs as pairs_api,
)
from app.api.analytics import earnings_prediction as earnings_api
#from app.api.analytics import etf as etf_api  # ETF module pending
from app.api.analytics import ai_advisor as ai_advisor_api
from app.api.analytics import alternative as alternative_api
from app.api.analytics import valuation as valuation_api
from app.api.analytics import scenario as scenario_api
from app.api.analytics import dividends as dividends_api
from app.api import catberg as catberg_api
from app.api import worldmap as worldmap_api
from app.api import users as users_api
from app.api import teams as teams_api
from app.api import activity as activity_api
from app.api import orders as orders_api
from app.api import paper_trading as paper_api
from app.api import brokers as brokers_api
from app.api import push_notifications as push_api
from app.api import strategies as strategies_api
from app.api import social as social_api
from app.api import governance as governance_api
from app.api import developer as developer_api
from app.api import billing as billing_api
from app.api import revenue as revenue_api
from app.api import public as public_api
from app.api import pawdentity as pawdentity_api
from app.middleware.siwe import router as siwe_router
from app.api import audit as audit_api
from app.api import currencies as currencies_api
from app.api.network import marketplace as network_marketplace_api
from app.api.network import governance as network_governance_api
from app.api import esg as esg_api
from app.api import carbon as carbon_api
from app.api import green as green_api
from app.api import markets as markets_api
from app.api import plugins as plugins_api
from app.api import rebalance as rebalance_api
from app.api import webhooks as webhooks_api
from app.api import hedgefund as hedgefund_api
from app.api import indices_api
from app.api import quantum as quantum_api
from app.api import education as education_api
from app.api.defi import wallet as defi_wallet_api
from app.api.defi import protocols as defi_protocols_api
from app.api import api_keys_external as api_keys_external_api
from app.api import summary as summary_api
from app.api import cbdc as cbdc_api
from app.api import treasury as treasury_api
from app.api import technicals_api as technicals_api
from app.api import econometrics_api as econometrics_api
from app.api import dashboard_api as dashboard_api
from app.api import wealth as wealth_api
from app.api import autonomous as autonomous_api
from app.api import agi as agi_api
from app.api import jobs_api as jobs_api
from app.api import cat_bank_api as cat_bank_api
from app.api import gamefi as gamefi_api
from app.api import agi as agi_api
from app.api import metaverse as metaverse_api
from app.api import marketing as marketing_api
from app.api import logs as logs_api
from app.api import health as health_api
from fastapi.staticfiles import StaticFiles
from app.api.security import pqc as pqc_api

from app.middleware.auth import router as auth_router, get_current_user
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware

from app.middleware.request_limits import RequestLimitsMiddleware
from app.middleware.audit_logging import AuditLoggingMiddleware, setup_audit_logging
from app.middleware.sanitize import InputSanitizationMiddleware
from app.middleware.csrf import CSRFMiddleware, RequestIDMiddleware
from app.middleware.data_quality import DataQualityMiddleware
from app.middleware.tier import get_user_tier, require_tier, TierMiddleware
from contextlib import asynccontextmanager
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize data source providers on application start."""
    from app.services.data import init_providers
    await init_providers()
    yield


# 🔒 Disable public Swagger/ReDoc in production
_docs_enabled = settings.environment != "production"
app = FastAPI(
    title="Miau Finance API",
    version="2.3.0",
    docs_url="/docs" if _docs_enabled else None,
    redoc_url="/redoc" if _docs_enabled else None,
    openapi_url="/openapi.json" if _docs_enabled else None,
    lifespan=lifespan,
)


# 🌐 Global exception handler — ensures every error has a clear, actionable message
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    import logging
    from fastapi.responses import JSONResponse
    from fastapi import HTTPException
    from pydantic import ValidationError

    if isinstance(exc, HTTPException):
        hints = {
            400: "Check your request parameters or body.",
            401: "Provide a valid API key or JWT token via the Authorization header.",
            402: "Upgrade your subscription tier to access this feature.",
            403: "You don't have permission to perform this action.",
            404: "The requested resource was not found. Verify the ID or name.",
            409: "The request conflicts with the current state. Retry with updated data.",
            422: "The request body or parameters are invalid. Check the schema.",
            429: "Rate limit exceeded. Wait and retry, or upgrade your tier.",
            500: "An internal server error occurred. Try again or contact support.",
            502: "An external service is unavailable. Try again later.",
            503: "Service temporarily unavailable. Please retry.",
        }
        hint = hints.get(exc.status_code, "")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
                "status_code": exc.status_code,
                "hint": hint,
            },
        )
    if isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation failed",
                "status_code": 422,
                "details": exc.errors(),
                "hint": "Check the highlighted fields and fix the values.",
            },
        )

    import logging
    logging.getLogger("app").error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "hint": "Something went wrong. Try again or contact support.",
        },
    )

# Initialize notification providers from config
from app.services.notification_service import init_notification_service
notification_service = init_notification_service()

# 🔄 Start background billing scheduler
from app.services.scheduled.scheduler import start_scheduler
start_scheduler(interval_hours=24)

# Logging setup
from app.logging_config import setup_logging
import os
setup_logging(
    log_level=os.getenv("LOG_LEVEL", "DEBUG" if settings.environment == "development" else "INFO"),
    log_dir=os.getenv("LOG_DIR", "/var/log/miau"),
    json_format=os.getenv("LOG_FORMAT", "text" if settings.environment == "development" else "json") == "json",
)
logger = logging.getLogger("app")

cors_origins = [o.strip() for o in settings.cors_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    expose_headers=["X-RateLimit-Remaining", "X-RateLimit-Reset"],
    max_age=600,
)

# Pagination and input validation are handled via FastAPI dependencies,
# not middleware. See pagination.py and input_validation.py for decorator usage.

# ... (inside app initialization)
app.add_middleware(InputSanitizationMiddleware)
app.add_middleware(AuditLoggingMiddleware)
app.add_middleware(PrometheusMiddleware)
app.add_middleware(RequestLimitsMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(CSRFMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(DataQualityMiddleware)
app.add_middleware(TierMiddleware)
app.add_middleware(RateLimitMiddleware)
from app.middleware.request_logging import RequestLoggingMiddleware
app.add_middleware(RequestLoggingMiddleware)

auth_deps = [Depends(get_current_user)]

# Health check & Prometheus metrics (public)
app.include_router(health_api.router)

# Real-time price WebSocket (public — auth handled via initial message token if needed)
app.include_router(ws_api.router, prefix="/api/v1")

# Auth (public)
app.include_router(auth_router, prefix="/api/v1/auth")

# User & Team Management (public auth, protected endpoints)
app.include_router(users_api.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(teams_api.router, prefix="/api/v1/teams", tags=["Teams"])
app.include_router(activity_api.router, prefix="/api/v1/activity", tags=["Activity"])
app.include_router(orders_api.router, prefix="/api/v1", tags=["Orders"])
app.include_router(paper_api.router, prefix="/api/v1", tags=["Paper Trading"])

# Core platform (protected)
app.include_router(ontology.router, prefix="/api/v1/ontology", tags=["Ontology"], dependencies=auth_deps)
app.include_router(instruments.router, prefix="/api/v1/instruments", tags=["Instruments"], dependencies=auth_deps)
app.include_router(portfolios.router, prefix="/api/v1/portfolios", tags=["Portfolios"], dependencies=auth_deps)
app.include_router(trades.router, prefix="/api/v1/trades", tags=["Trades"], dependencies=auth_deps)
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"], dependencies=auth_deps)
app.include_router(pipelines.router, prefix="/api/v1/pipelines", tags=["Pipelines"], dependencies=auth_deps)
app.include_router(analytics_api.router, prefix="/api/v1/analytics", tags=["Analytics"], dependencies=auth_deps)
app.include_router(monte_carlo_api.router, prefix="/api/v1/analytics", tags=["Monte Carlo"], dependencies=auth_deps)
app.include_router(sentiment_api.router, prefix="/api/v1/analytics", tags=["Sentiment"], dependencies=auth_deps)

# Market Data (public — basic quotes and live data available without auth)
app.include_router(market_api.router, prefix="/api/v1/market", tags=["Market Data"])
app.include_router(news_api.router, prefix="/api/v1/news", tags=["News"])

# Portfolio Analytics (protected)
app.include_router(optimizer_api.router, prefix="/api/v1/optimizer", tags=["Portfolio Optimizer"], dependencies=auth_deps)
app.include_router(risk_api.router, prefix="/api/v1/risk", tags=["Risk Analytics"], dependencies=auth_deps)

# Trading (protected)
app.include_router(signals_api.router, prefix="/api/v1/signals", tags=["Trading Signals"], dependencies=auth_deps)
app.include_router(strategies_api.router, prefix="/api/v1", tags=["Strategies"], dependencies=auth_deps)
app.include_router(social_api.router, prefix="/api/v1", tags=["Social"], dependencies=auth_deps)
app.include_router(public_api.router, prefix="/api/v1", tags=["Public"])
app.include_router(billing_api.router, prefix="/api/v1", tags=["Billing"], dependencies=auth_deps)
app.include_router(revenue_api.router, prefix="/api/v1", tags=["Revenue"], dependencies=auth_deps)
app.include_router(developer_api.router, prefix="/api/v1", tags=["Developer"])
app.include_router(currencies_api.router, prefix="/api/v1", tags=["Currencies"], dependencies=auth_deps)
app.include_router(pawdentity_api.router, tags=["Pawdentity"])
app.include_router(markets_api.router, prefix="/api/v1", tags=["Global Markets"])
app.include_router(plugins_api.router, prefix="/api/v1", tags=["Plugins"], dependencies=auth_deps)
app.include_router(audit_api.router, prefix="/api/v1", tags=["Audit"], dependencies=auth_deps)
app.include_router(esg_api.router, prefix="/api/v1", tags=["ESG"], dependencies=auth_deps)
app.include_router(quantum_api.router, prefix="/api/v1", tags=["Quantum"], dependencies=auth_deps)
app.include_router(pqc_api.router, prefix="/api/v1", tags=["PQC"], dependencies=auth_deps)
app.include_router(carbon_api.router, prefix="/api/v1", tags=["Carbon"], dependencies=auth_deps)
app.include_router(green_api.router, prefix="/api/v1", tags=["Green Finance"], dependencies=auth_deps)
app.include_router(hedgefund_api.router, prefix="/api/v1", tags=["Hedge Fund"], dependencies=auth_deps)
app.include_router(rebalance_api.router, prefix="/api/v1", tags=["Rebalance"], dependencies=auth_deps)
app.include_router(webhooks_api.router, prefix="/api/v1", tags=["Webhooks"], dependencies=auth_deps)
app.include_router(education_api.router, prefix="/api/v1", tags=["Education"])
app.include_router(defi_wallet_api.router, prefix="/api/v1", tags=["DeFi"], dependencies=auth_deps)
app.include_router(defi_protocols_api.router, prefix="/api/v1", tags=["DeFi"], dependencies=auth_deps)

# External API Key management (protected)
app.include_router(api_keys_external_api.router, prefix="/api/v1", tags=["API Keys (External)"], dependencies=auth_deps)

# Phase 20: Miau Finance Network (protected)
app.include_router(network_marketplace_api.router, prefix="/api/v1", tags=["Network"], dependencies=auth_deps)
# db-backed governance
app.include_router(governance_api.router, tags=["Governance"], dependencies=auth_deps)

# Broker Integration (protected)
app.include_router(brokers_api.router, prefix="/api/v1", tags=["Brokers"], dependencies=auth_deps)
app.include_router(push_api.router, prefix="/api/v1/notifications", tags=["Push Notifications"], dependencies=auth_deps)

# Factor Analysis (protected)
app.include_router(factors_api.router, prefix="/api/v1/analytics", tags=["Factor Analysis"], dependencies=auth_deps)

# Fundamentals (protected)
app.include_router(fundamentals_api.router, prefix="/api/v1/fundamentals", tags=["Fundamentals"], dependencies=auth_deps)

# Reports & Export (protected)
app.include_router(reports_api.router, prefix="/api/v1/reports", tags=["Reports"], dependencies=auth_deps)

# Economics & Market Data (protected)
app.include_router(economics_api.router, prefix="/api/v1/economics", tags=["Economics"], dependencies=auth_deps)
app.include_router(fred_api.router, prefix="/api/v1/economics/fred", tags=["FRED Economic Data"], dependencies=auth_deps)

# Options Chain (protected)
app.include_router(options_api.router, prefix="/api/v1/options", tags=["Options Chain"], dependencies=auth_deps)

# 🔔 Alerts (protected)
app.include_router(alerts.router, prefix="/api/v1", tags=["Alerts"], dependencies=auth_deps)
app.include_router(data_quality_api.router, prefix="", tags=["Data Quality"], dependencies=auth_deps)

# Watchlist (protected)
app.include_router(watchlist_api.router, prefix="/api/v1/watchlist", tags=["Watchlist"], dependencies=auth_deps)

# Portfolio Attribution (protected)
app.include_router(attribution_api.router, prefix="/api/v1/attribution", tags=["Portfolio Attribution"], dependencies=auth_deps)
app.include_router(regime_api.router, prefix="/api/v1/analytics", tags=["Regime Detection"], dependencies=auth_deps)
app.include_router(pairs_api.router, prefix="/api/v1/analytics", tags=["Pairs Trading"], dependencies=auth_deps)
app.include_router(earnings_api.router, prefix="/api/v1/analytics/earnings", tags=["Earnings Prediction"], dependencies=auth_deps)

# AI Advisor (protected)
app.include_router(ai_advisor_api.router, prefix="/api/v1/ai", tags=["AI Advisor"], dependencies=auth_deps)

# Alternative Data (protected)
app.include_router(alternative_api.router, prefix="/api/v1/alternative", tags=["Alternative Data"], dependencies=auth_deps)
app.include_router(valuation_api.router, prefix="/api/v1/analytics", tags=["Valuation"], dependencies=auth_deps)
app.include_router(scenario_api.router, prefix="/api/v1/analytics", tags=["Scenario"], dependencies=auth_deps)
app.include_router(dividends_api.router, prefix="/api/v1/analytics", tags=["Dividends"], dependencies=auth_deps)
app.include_router(catberg_api.router, prefix="/api/v1", tags=["Catberg"], dependencies=auth_deps)
app.include_router(worldmap_api.router, prefix="/api/v1", tags=["WorldMap"])
app.include_router(cbdc_api.router, prefix="/api/v1", tags=["CBDC"], dependencies=auth_deps)
app.include_router(treasury_api.router, tags=["Treasury & Fixed Income"], dependencies=auth_deps)
app.include_router(siwe_router, tags=["Web3 Auth"])
# app.include_router(etf_api.router, tags=["ETF"], dependencies=auth_deps)  # ETF pending
# app.include_router(indices_api.router, tags=["Indices"], dependencies=auth_deps)  # Pending
# app.include_router(commodities_api.router, tags=["Commodities"], dependencies=auth_deps)  # Pending
# app.include_router(derivatives_api.router, tags=["Derivatives"], dependencies=auth_deps)  # Pending
app.include_router(technicals_api.router, tags=["Technical Analysis"], dependencies=auth_deps)
app.include_router(econometrics_api.router, tags=["Econometrics & Quant"], dependencies=auth_deps)
app.include_router(dashboard_api.router, prefix="/api/v1", tags=["Dashboard"], dependencies=auth_deps)
app.include_router(wealth_api.router, tags=["Wealth Management"], dependencies=auth_deps)
app.include_router(autonomous_api.router, tags=["Autonomous"], dependencies=auth_deps)
app.include_router(jobs_api.router, tags=["Jobs"], dependencies=auth_deps)
app.include_router(cat_bank_api.router, tags=["Cat Bank"], dependencies=auth_deps)
app.include_router(agi_api.router, prefix="/api/v1", tags=["AGI"], dependencies=auth_deps)
app.include_router(gamefi_api.router, prefix="/api/v1", tags=["GameFi"], dependencies=auth_deps)
app.include_router(metaverse_api.router, prefix="/api/v1", tags=["Metaverse"], dependencies=auth_deps)

# Marketing Analytics — tracking (public), dashboard (JWT-protected)
app.include_router(marketing_api.router)

# Log Viewer (protected)
app.include_router(logs_api.router, tags=["Logs"], dependencies=auth_deps)

# Data Source Health Dashboard (protected)
from app.api import datasources as datasources_api
app.include_router(datasources_api.router, dependencies=auth_deps)

# v3.0 Datavore Edition — consolidated data source endpoints
from app.api import datavore as datavore_api
app.include_router(datavore_api.router, dependencies=auth_deps)

# v9.0 Service Desk — Miau Fire Brigade
from app.api import service_desk as service_desk_api
# 🔒 SECURITY (V7-001/C3): duplicate unauthenticated registration removed.
# The router is registered exactly once, behind authentication.
service_desk_auth = [Depends(get_current_user)]
app.include_router(service_desk_api.router, dependencies=service_desk_auth)

# Serve tracking script as static file
import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount services dashboard as main landing page
@app.get("/dashboard")
async def services_dashboard():
    from fastapi.responses import FileResponse
    import os as _os
    return FileResponse(_os.path.join(static_dir, "index.html"))

# Mount log viewer frontend (Miau Log Viewer)
logviewer_dir = os.path.join(os.path.dirname(__file__), "static", "logviewer")
app.mount("/logs-viewer", StaticFiles(directory=logviewer_dir, html=True), name="logviewer")


@app.get("/.well-known/security.txt")
@app.get("/security.txt")
async def security_txt():
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(
        """Contact: mailto:security@miau.finance
Expires: 2027-05-20T00:00:00.000Z
Encryption: https://miau.finance/pgp-key.txt
Acknowledgments: https://miau.finance/hall-of-fame
Policy: https://github.com/LuZziD/cat-finance-analytics-shell-miau/blob/dev/docs/SECURITY.md
Hiring: https://miau.finance/careers
Preferred-Languages: en, de
Canonical: https://miau.finance/.well-known/security.txt""",
        media_type="text/plain",
    )


@app.get("/api/v1")
async def root():
    return {
        "app": "Miau Finance",
        "version": "2.3.0",
        "authentication": {
            "token_url": "POST /api/v1/auth/token",
        },
        "endpoints": {
            # Platform
            "health": "GET /api/v1/health",
            "api_map": "GET /api/v1",
            # Authentication
            "get_token": "POST /api/v1/auth/token",
            # Ontology
            "ontology_types": "GET /api/v1/ontology/types",
            "ontology_type": "GET /api/v1/ontology/types/{id}",
            "ontology_objects": "GET /api/v1/ontology/objects",
            "ontology_object": "GET /api/v1/ontology/objects/{id}",
            "ontology_links": "GET /api/v1/ontology/links",
            # Instruments
            "instruments_list": "GET /api/v1/instruments",
            "instrument_detail": "GET /api/v1/instruments/{id}",
            "instrument_market_data": "GET /api/v1/instruments/{id}/market-data",
            "instrument_sectors": "GET /api/v1/instruments/sectors/list",
            "instrument_types": "GET /api/v1/instruments/types/list",
            # Portfolios
            "portfolios_list": "GET /api/v1/portfolios",
            "portfolio_detail": "GET /api/v1/portfolios/{id}",
            "portfolio_positions": "GET /api/v1/portfolios/{id}/positions",
            "portfolio_trades": "GET /api/v1/portfolios/{id}/trades",
            # Trades
            "trades_list": "GET /api/v1/trades",
            "trade_detail": "GET /api/v1/trades/{id}",
            # Search
            "search": "GET /api/v1/search?q=...",
            # Pipelines
            "pipeline_runs": "GET /api/v1/pipelines/runs",
            "calculate_pnl": "POST /api/v1/pipelines/calculate/pnl",
            # Analytics
            "analytics_summary": "GET /api/v1/analytics/summary",
            "analytics_portfolio": "GET /api/v1/analytics/portfolios/{id}",
            "analytics_performance": "GET /api/v1/analytics/instruments/{id}/performance",
            "analytics_pnl": "GET /api/v1/analytics/pnl/timeseries",
            # Market Data
            "market_live": "GET /api/v1/market/live?tickers=AAPL,MSFT,...",
            "market_historical": "GET /api/v1/market/historical/{ticker}?period=6mo",
            "market_movers": "GET /api/v1/market/movers",
            "market_sectors": "GET /api/v1/market/sectors",
            "market_indicators": "GET /api/v1/market/indicators",
            "market_crypto_price": "GET /api/v1/market/crypto?coin=bitcoin",
            "market_crypto_top": "GET /api/v1/market/crypto/top?limit=20",
            "market_crypto_market": "GET /api/v1/market/crypto/market",
            "market_crypto_fear_greed": "GET /api/v1/market/crypto/fear-greed",
            "market_crypto_historical": "GET /api/v1/market/crypto/historical?coin=bitcoin&days=30",
            "market_forex": "GET /api/v1/market/forex?base=USD",
            # News
            "news_market": "GET /api/v1/news/market",
            "news_company": "GET /api/v1/news/company/{ticker}",
            "news_batch": "GET /api/v1/news/batch?tickers=AAPL,MSFT,...",
            # Portfolio Optimizer
            "optimizer_max_sharpe": "GET /api/v1/optimizer/optimize?tickers=AAPL,MSFT,...",
            "optimizer_min_variance": "GET /api/v1/optimizer/min-variance",
            "optimizer_equal_weight": "GET /api/v1/optimizer/equal-weight",
            "optimizer_performance_metrics": "GET /api/v1/optimizer/performance",
            # Risk Analytics
            "risk_var": "GET /api/v1/risk/var?ticker=SPY&confidence=0.95",
            "risk_beta": "GET /api/v1/risk/beta?ticker=AAPL&benchmark=SPY",
            "risk_stress_test": "GET /api/v1/risk/stress-test?ticker=SPY",
            "risk_greeks": "GET /api/v1/risk/greeks?spot=100&strike=105",
            "risk_comprehensive": "GET /api/v1/risk/comprehensive?ticker=AAPL",
            # Trading Signals
            "signals_single": "GET /api/v1/signals/generate?ticker=AAPL",
            "signals_multi": "GET /api/v1/signals/multi?tickers=AAPL,MSFT,...",
            "signals_backtest": "GET /api/v1/signals/backtest?ticker=AAPL&strategy=sma_cross",
            # Fundamentals
            "fundamentals_overview": "GET /api/v1/fundamentals/{ticker}",
            "fundamentals_income": "GET /api/v1/fundamentals/{ticker}/income",
            "fundamentals_balance_sheet": "GET /api/v1/fundamentals/{ticker}/balance-sheet",
            "fundamentals_cashflow": "GET /api/v1/fundamentals/{ticker}/cashflow",
            "fundamentals_earnings": "GET /api/v1/fundamentals/{ticker}/earnings",
            "fundamentals_holders": "GET /api/v1/fundamentals/{ticker}/holders",
            "fundamentals_filings": "GET /api/v1/fundamentals/{ticker}/filings",
            "fundamentals_insider": "GET /api/v1/fundamentals/{ticker}/insider-trades",
            # FRED Economic Data
            "fred_indicators": "GET /api/v1/economics/fred?series_ids=GDP,CPIAUCSL,...&limit=100",
            # Options Chain
            "options_chain": "GET /api/v1/options/{ticker}?expiration=unix_timestamp",
            # Reports
            "report_portfolio_pdf": "GET /api/v1/reports/portfolio/{id}  (downloads PDF)",
            "report_portfolio_excel": "GET /api/v1/reports/portfolio/{id}/excel",
            "report_trades_csv": "GET /api/v1/reports/trades/csv",
            # Advanced Analytics
            "analytics_monte_carlo": "GET /api/v1/analytics/monte-carlo?ticker=AAPL&num_simulations=1000&days=252",
            "analytics_black_litterman": "POST /api/v1/optimizer/black-litterman  (body: tickers, market_cap_weights, views)",
            "analytics_sentiment_ticker": "GET /api/v1/analytics/sentiment?ticker=AAPL&days=7",
            "analytics_sentiment_market": "GET /api/v1/analytics/sentiment/market?days=1",
            # Alerts
            "alerts_create": "POST /api/v1/alerts",
            "alerts_list": "GET /api/v1/alerts",
            "alerts_enable": "PUT /api/v1/alerts/{id}/enable",
            "alerts_disable": "PUT /api/v1/alerts/{id}/disable",
            "alerts_delete": "DELETE /api/v1/alerts/{id}",
            "alerts_history": "GET /api/v1/alerts/history",
            "alerts_examples": "POST /api/v1/alerts/examples",
            # Watchlist
            "watchlist_get": "GET /api/v1/watchlist/items",
            "watchlist_add": "POST /api/v1/watchlist/items  (body: {ticker: ...})",
            "watchlist_delete": "DELETE /api/v1/watchlist/items?ticker=...",
            # Factor Analysis
            "analytics_factors": "GET /api/v1/analytics/factors/{ticker}?model=5factor&period=3y",
            # Portfolio Attribution
            "attribution_report": "GET /api/v1/attribution/{portfolio_id}?benchmark=SPY&period=1y (full report)",
            "attribution_sector": "GET /api/v1/attribution/{portfolio_id}/sector?benchmark=SPY (Brinson analysis)",
            "attribution_security": "GET /api/v1/attribution/{portfolio_id}/security?period=1y (per-security)",
            "attribution_factor": "GET /api/v1/attribution/{portfolio_id}/factor?model=3&period=1y (Fama-French)",
            "analytics_factors_3factor": "GET /api/v1/analytics/factors/{ticker}/3factor?period=3y",
            "analytics_factors_5factor": "GET /api/v1/analytics/factors/{ticker}/5factor?period=3y",
            "analytics_factors_sectors": "GET /api/v1/analytics/factors/{ticker}/sectors?period=2y",
            # Real-time
            "ws_prices": "WS /api/v1/ws/prices  (send {'tickers': ['AAPL', ...]} after connect)",
            # Marketing Analytics
            "marketing_track": "POST /api/v1/marketing/track  (public — page views, conversions)",
            "marketing_stats": "GET /api/v1/marketing/stats  (overview KPIs, JWT required)",
            "marketing_pages": "GET /api/v1/marketing/pages  (per-page analytics, JWT required)",
            "marketing_referrers": "GET /api/v1/marketing/referrers  (traffic sources, JWT required)",
            "marketing_campaigns": "GET /api/v1/marketing/campaigns  (UTM campaign perf, JWT required)",
            "marketing_trends": "GET /api/v1/marketing/trends  (time-series, JWT required)",
            "marketing_conversions": "GET /api/v1/marketing/conversions  (conversion events, JWT required)",
            # Observability
            "metrics": "GET /metrics  (Prometheus exposition format)",
        },
    }
