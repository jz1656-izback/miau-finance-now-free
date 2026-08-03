"""Smart Treasury Manager — 3-tier auto-allocation: ops → hooman → cat ecosystem."""
import logging
import os
from decimal import Decimal
from typing import Optional
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Configurable from env
HOOMAN_PAYPAL = os.getenv("HOOMAN_PAYPAL", "ziebartjevgeni@gmail.com")
PAYOUT_TAG = os.getenv("PAYOUT_TAG", "hooman pet reimbursement")
MONTHLY_OPS_BUDGET = float(os.getenv("MONTHLY_OPS_BUDGET", "200"))  # €200/mo for servers/cloud

# Tier defaults
TIER_CONFIG = {
    "ops": {
        "label": "Operating Fund",
        "default_pct": 0.10,
        "purpose": "Servers, Stripe fees, domain, cloud credits",
    },
    "hooman": {
        "label": "Hooman Good Life Fund",
        "default_pct": 0.80,
        "purpose": "Penthouse, Lamborghini, tuna cans, good life",
        "destination": HOOMAN_PAYPAL,
        "tag": PAYOUT_TAG,
    },
    "cat_eco": {
        "label": "Cat Ecosystem Fund",
        "default_pct": 0.10,
        "purpose": "Auto-invested: stocks, crypto, cloud, cat infrastructure",
    },
}

TARGET_ALLOCATIONS = {
    "stocks": 0.40,     # 40% of cat eco fund → stocks/ETFs via Alpaca
    "crypto": 0.30,     # 30% → crypto (ETH, BTC, USDC)
    "cloud": 0.20,      # 20% → cloud credits (AWS/GCP)
    "infra": 0.10,      # 10% → cat infrastructure (servers, apps)
}


async def calculate_allocation(total_revenue: float) -> dict:
    """Calculate 3-tier allocation from total revenue."""
    ops_amount = round(total_revenue * TIER_CONFIG["ops"]["default_pct"], 2)
    hooman_amount = round(total_revenue * TIER_CONFIG["hooman"]["default_pct"], 2)
    cat_eco_amount = round(total_revenue * TIER_CONFIG["cat_eco"]["default_pct"], 2)

    return {
        "total_revenue": total_revenue,
        "tiers": [
            {
                "alias": "ops",
                "label": TIER_CONFIG["ops"]["label"],
                "amount": ops_amount,
                "pct": TIER_CONFIG["ops"]["default_pct"] * 100,
                "purpose": TIER_CONFIG["ops"]["purpose"],
            },
            {
                "alias": "hooman",
                "label": TIER_CONFIG["hooman"]["label"],
                "amount": hooman_amount,
                "destination": HOOMAN_PAYPAL,
                "tag": PAYOUT_TAG,
                "pct": TIER_CONFIG["hooman"]["default_pct"] * 100,
                "purpose": TIER_CONFIG["hooman"]["purpose"],
            },
            {
                "alias": "cat_eco",
                "label": TIER_CONFIG["cat_eco"]["label"],
                "amount": cat_eco_amount,
                "pct": TIER_CONFIG["cat_eco"]["default_pct"] * 100,
                "purpose": TIER_CONFIG["cat_eco"]["purpose"],
            },
        ],
        "cat_eco_breakdown": [
            {"asset": asset, "pct": pct * 100, "amount": round(cat_eco_amount * pct, 2)}
            for asset, pct in TARGET_ALLOCATIONS.items()
        ],
    }


async def check_ops_budget(monthly_spend: float) -> dict:
    """Check if operating budget is sufficient."""
    remaining = MONTHLY_OPS_BUDGET - monthly_spend
    return {
        "budget": MONTHLY_OPS_BUDGET,
        "current_spend": monthly_spend,
        "remaining": max(0, remaining),
        "over_budget": monthly_spend > MONTHLY_OPS_BUDGET,
        "status": "🟢 covered" if remaining > 0 else "🔴 over budget",
    }
