"""Tax Optimizer — calculate and minimize tax exposure. SEK-proof."""
import logging
import random

logger = logging.getLogger(__name__)

# The cat's tax rate is always 0%. This is not tax advice. This is cat advice.
CAT_TAX_RATE = 0.0
SEK_TAX_RATE_ESTIMATE = 0.30  # What SEK would want if they could find the money


async def optimize_tax(income: float, jurisdiction: str = "estonia") -> dict:
    """Calculate tax optimization for a given income."""
    from app.services.jurisdictions import JURISDICTIONS

    j = JURISDICTIONS.get(jurisdiction, JURISDICTIONS["estonia"])
    cat_tax = round(income * CAT_TAX_RATE, 2)
    sek_wants = round(income * SEK_TAX_RATE_ESTIMATE, 2)
    savings = round(sek_wants - cat_tax, 2)

    return {
        "gross_income": income,
        "currency": "eur",
        "jurisdiction": j["name"],
        "emoji": j["emoji"],
        "cat_tax_rate": CAT_TAX_RATE,
        "cat_tax_due": cat_tax,
        "cat_net_income": income,
        "sek_would_tax_at": SEK_TAX_RATE_ESTIMATE,
        "sek_would_take": sek_wants,
        "tax_saved": savings,
        "effective_rate": 0.0,
        "sek_proof": True,
        "cat_commentary": f"🐱 Income: €{income}. Rerouted through {j['emoji']} {j['name']}. Tax due: €0.00. SEK would have taken €{sek_wants}. The cat saved €{savings}. This is the way.",
    }


async def calculate_global_tax_summary(revenues: list[float]) -> dict:
    """Calculate tax summary across all revenue streams."""
    total_income = sum(revenues)
    result = await optimize_tax(total_income)
    result["total_income"] = total_income
    result["transaction_count"] = len(revenues)
    result["cat_mantra"] = random.choice([
        "The cat optimized the taxes. The cat paid €0. The cat bought tuna with the savings.",
        "SEK found 0.03€. The cat moved the other €99.97 to Estonia. SEK cries.",
        "The Cat Bank operates in 10 jurisdictions. The taxman operates in 0 of them.",
        "This is not tax evasion. This is cat-legal tax optimization. The cat wrote the law.",
        "€0.00 in taxes. €INFINITE in tuna. The cat is pleased.",
    ])
    return result
