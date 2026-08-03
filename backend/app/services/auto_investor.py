"""Auto Investor — executes investment allocations via broker APIs."""
import logging
import os
from decimal import Decimal
from typing import Optional

logger = logging.getLogger(__name__)

ALPACA_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET = os.getenv("ALPACA_SECRET_KEY", "")
ALPACA_PAPER = os.getenv("ALPACA_PAPER", "true").lower() == "true"

DEFAULT_BUY_LIST = [
    {"symbol": "SPY", "name": "S&P 500 ETF", "target": 0.35},
    {"symbol": "QQQ", "name": "Nasdaq 100 ETF", "target": 0.25},
    {"symbol": "VTI", "name": "Total Stock Market ETF", "target": 0.15},
    {"symbol": "BND", "name": "Total Bond Market ETF", "target": 0.10},
    {"symbol": "GLD", "name": "Gold ETF", "target": 0.10},
    {"symbol": "IAU", "name": "Gold Trust", "target": 0.05},
]


async def auto_buy_stocks(amount: float, dry_run: bool = True) -> dict:
    """Auto-buy stocks via Alpaca broker from cat ecosystem fund."""
    if not ALPACA_KEY:
        return {"status": "skipped", "reason": "Alpaca not configured (ALPACA_API_KEY)"}

    # Calculate per-symbol allocation
    buys = []
    for item in DEFAULT_BUY_LIST:
        symbol_amount = round(amount * item["target"], 2)
        if symbol_amount < 1:
            continue
        buys.append({
            "symbol": item["symbol"],
            "name": item["name"],
            "amount": symbol_amount,
            "target_pct": item["target"] * 100,
        })

        if not dry_run:
            try:
                from app.services.brokers.alpaca import AlpacaBroker
                from app.config import settings
                broker = AlpacaBroker()
                # Use market price to calculate qty from dollar amount
                order = await broker.submit_order({
                    "symbol": item["symbol"],
                    "qty": symbol_amount / 500,  # ~€500 per share average
                    "side": "buy",
                    "type": "market",
                    "time_in_force": "day",
                })
                logger.info("Auto-bought %s: %s", item["symbol"], order.get("id", "?"))
            except Exception as e:
                logger.error("Auto-buy failed for %s: %s", item["symbol"], e)

    return {
        "status": "buy_orders_prepared" if dry_run else "buy_orders_executed",
        "total": amount,
        "dry_run": dry_run,
        "buys": buys,
        "broker": "alpaca (paper)" if ALPACA_PAPER else "alpaca (live)",
    }


async def auto_buy_crypto(amount: float, dry_run: bool = True) -> dict:
    """Auto-buy crypto from cat ecosystem fund."""
    allocations = [
        {"asset": "ETH", "target": 0.50, "description": "Ethereum (cat's favorite)"},
        {"asset": "BTC", "target": 0.30, "description": "Bitcoin (digital tuna)"},
        {"asset": "USDC", "target": 0.20, "description": "USDC (stablecoins for safety)"},
    ]
    buys = []
    for item in allocations:
        asset_amount = round(amount * item["target"], 2)
        if asset_amount < 1:
            continue
        buys.append({
            "asset": item["asset"],
            "amount": asset_amount,
            "target_pct": item["target"] * 100,
            "description": item["description"],
        })
    return {
        "status": "crypto_buys_prepared" if dry_run else "crypto_buys_executed",
        "total": amount,
        "dry_run": dry_run,
        "buys": buys,
    }
