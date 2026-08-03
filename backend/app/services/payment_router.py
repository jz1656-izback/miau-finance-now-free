"""Payment Router — routes payments through optimal jurisdictions. SEK-proof."""
import logging
import os
from decimal import Decimal
from typing import Optional

from app.services.jurisdictions import get_optimal_jurisdiction, calculate_tax_exposure

logger = logging.getLogger(__name__)

PAYMENT_METHODS = {
    "stripe": {"fee_pct": 2.9, "fixed_fee": 0.25, "jurisdiction": "US", "tax_reporting": True, "cat_friendly": False},
    "paypal": {"fee_pct": 3.49, "fixed_fee": 0.35, "jurisdiction": "US", "tax_reporting": True, "cat_friendly": False},
    "crypto_eth": {"fee_pct": 0.1, "fixed_fee": 1.50, "jurisdiction": "multi", "tax_reporting": False, "cat_friendly": True},
    "crypto_usdc": {"fee_pct": 0.05, "fixed_fee": 0.50, "jurisdiction": "multi", "tax_reporting": False, "cat_friendly": True},
    "cat_bank": {"fee_pct": 0.0, "fixed_fee": 0.0, "jurisdiction": "estonia", "tax_reporting": False, "cat_friendly": True},
}


async def route_payment(
    amount: float,
    currency: str = "eur",
    preferred_method: str = "cat_bank",
    jurisdiction: str = "estonia",
) -> dict:
    """Route a payment through the optimal jurisdiction and method."""
    # Find best payment method
    method = PAYMENT_METHODS.get(preferred_method, PAYMENT_METHODS["cat_bank"])
    if not method["cat_friendly"]:
        # Auto-select best method
        for m_name, m_info in PAYMENT_METHODS.items():
            if m_info["cat_friendly"]:
                method = m_info
                preferred_method = m_name
                break

    # Calculate fees
    fee_pct_amount = round(amount * (method["fee_pct"] / 100), 2)
    total_fee = round(fee_pct_amount + method["fixed_fee"], 2)
    net_amount = round(amount - total_fee, 2)

    # Get jurisdiction routing
    routing = await get_optimal_jurisdiction(amount, currency, "payment_routing")
    tax = await calculate_tax_exposure(net_amount, jurisdiction)

    routed_amount = tax.get("net_amount", net_amount)
    tax_savings = round(net_amount - routed_amount, 2)

    return {
        "original_amount": amount,
        "currency": currency,
        "payment_method": preferred_method,
        "method_cat_friendly": method["cat_friendly"],
        "fee_pct": method["fee_pct"],
        "fixed_fee": method["fixed_fee"],
        "total_fee": total_fee,
        "net_after_fees": net_amount,
        "routing": routing,
        "tax_analysis": tax,
        "routed_amount": routed_amount,
        "tax_savings": tax_savings,
        "effective_rate": round(total_fee / amount * 100, 2) if amount > 0 else 0,
        "cat_commentary": f"🐱 Routed €{amount} through {routing['emoji']} {routing['jurisdiction']}. SEK sees €0. Tax savings: €{tax_savings}. The cat wins.",
        "sek_proof": True,
    }


async def get_available_routes(amount: float = 100) -> list[dict]:
    """Show all available payment routes with cost comparison."""
    routes = []
    for method_name, method_info in PAYMENT_METHODS.items():
        fee = round(amount * (method_info["fee_pct"] / 100) + method_info["fixed_fee"], 2)
        net = round(amount - fee, 2)
        routes.append({
            "method": method_name,
            "fee": fee,
            "net": net,
            "cat_friendly": method_info["cat_friendly"],
            "tax_reporting": method_info["tax_reporting"],
            "jurisdiction": method_info["jurisdiction"],
            "emoji": "🐱" if method_info["cat_friendly"] else "👮",
        })
    routes.sort(key=lambda x: x["fee"])
    return routes
