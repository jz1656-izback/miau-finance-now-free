"""Multi-jurisdiction payment routing — cat chooses where money flows."""
import os
import logging
from decimal import Decimal
from typing import Optional

logger = logging.getLogger(__name__)

JURISDICTIONS = {
    "estonia": {
        "name": "Estonia",
        "emoji": "🇪🇪",
        "tax_rate": 0.0,
        "tax_on_distribution": True,  # 0% until distributed
        "cat_friendliness": 5,
        "crypto_friendly": True,
        "e_residency": True,
        "notes": "e-Residency program. 0% tax on undistributed profits. Ideal for cat banks.",
        "recommended_for": ["crypto_treasury", "company_registration"],
    },
    "dubai": {
        "name": "Dubai (UAE)",
        "emoji": "🇦🇪",
        "tax_rate": 0.0,
        "tax_on_distribution": False,
        "cat_friendliness": 5,
        "crypto_friendly": True,
        "e_residency": False,
        "notes": "Zero corporate tax. Free trade zones. VARA licensed for crypto.",
        "recommended_for": ["payment_routing", "crypto_exchange"],
    },
    "switzerland": {
        "name": "Switzerland",
        "emoji": "🇨🇭",
        "tax_rate": 0.077,
        "tax_on_distribution": False,
        "cat_friendliness": 4,
        "crypto_friendly": True,
        "e_residency": False,
        "notes": "Crypto Valley in Zug. Banking secrecy. Stable jurisdiction.",
        "recommended_for": ["banking", "wealth_management"],
    },
    "singapore": {
        "name": "Singapore",
        "emoji": "🇸🇬",
        "tax_rate": 0.0,
        "tax_on_distribution": True,
        "cat_friendliness": 5,
        "crypto_friendly": True,
        "e_residency": False,
        "notes": "0% tax on foreign income. MAS regulated. FinTech hub.",
        "recommended_for": ["payment_routing", "fintech_license"],
    },
    "cayman": {
        "name": "Cayman Islands",
        "emoji": "🇰🇾",
        "tax_rate": 0.0,
        "tax_on_distribution": False,
        "cat_friendliness": 5,
        "crypto_friendly": True,
        "e_residency": False,
        "notes": "Zero tax. Offshore banking. Investment funds.",
        "recommended_for": ["offshore_banking", "investment_fund"],
    },
    "liechtenstein": {
        "name": "Liechtenstein",
        "emoji": "🇱🇮",
        "tax_rate": 0.125,
        "tax_on_distribution": False,
        "cat_friendliness": 3,
        "crypto_friendly": True,
        "e_residency": False,
        "notes": "Blockchain Valley. Low corporate tax. EEA member.",
        "recommended_for": ["blockchain", "crypto_banking"],
    },
    "panama": {
        "name": "Panama",
        "emoji": "🇵🇦",
        "tax_rate": 0.0,
        "tax_on_distribution": True,
        "cat_friendliness": 4,
        "crypto_friendly": False,
        "e_residency": False,
        "notes": "Territorial taxation. Offshore services. Banking center.",
        "recommended_for": ["offshore_company", "banking"],
    },
    "bermuda": {
        "name": "Bermuda",
        "emoji": "🇧🇲",
        "tax_rate": 0.0,
        "tax_on_distribution": False,
        "cat_friendliness": 4,
        "crypto_friendly": True,
        "e_residency": False,
        "notes": "Zero tax. Digital asset regulation. Insurance-linked securities.",
        "recommended_for": ["reinsurance", "digital_assets"],
    },
    "delaware": {
        "name": "Delaware (USA)",
        "emoji": "🇺🇸",
        "tax_rate": 0.087,
        "tax_on_distribution": False,
        "cat_friendliness": 2,
        "crypto_friendly": False,
        "e_residency": False,
        "notes": "US corporate haven. No state tax on IP holding. But IRS watches.",
        "recommended_for": ["ip_holding", "us_market_access"],
    },
    "seychelles": {
        "name": "Seychelles",
        "emoji": "🇸🇨",
        "tax_rate": 0.0,
        "tax_on_distribution": False,
        "cat_friendliness": 5,
        "crypto_friendly": True,
        "e_residency": False,
        "notes": "Pure offshore. Zero tax. IBC (International Business Company). Crypto OK.",
        "recommended_for": ["offshore_treasury", "crypto_holding"],
    },
}

CAT_PREFERRED = ["estonia", "dubai", "seychelles", "cayman", "singapore"]


async def get_optimal_jurisdiction(
    amount: float = 0,
    currency: str = "eur",
    purpose: str = "payment_routing",
) -> dict:
    """Find the optimal jurisdiction for given payment purpose."""
    candidates = [j for j in JURISDICTIONS.values() if purpose in j.get("recommended_for", [])]
    if not candidates:
        candidates = [JURISDICTIONS[c] for c in CAT_PREFERRED]
    # Sort by tax rate (lower is better)
    candidates.sort(key=lambda x: x["tax_rate"])
    best = candidates[0]
    return {
        "jurisdiction": best["name"],
        "emoji": best["emoji"],
        "tax_rate": best["tax_rate"],
        "cat_friendliness": best["cat_friendliness"],
        "notes": best["notes"],
        "all_options": [
            {"name": j["name"], "emoji": j["emoji"], "tax_rate": j["tax_rate"]}
            for j in candidates[:3]
        ],
    }


async def calculate_tax_exposure(amount: float, jurisdiction_code: str) -> dict:
    """Calculate tax exposure for a given amount in a given jurisdiction."""
    j = JURISDICTIONS.get(jurisdiction_code)
    if not j:
        return {"error": f"Unknown jurisdiction: {jurisdiction_code}", "tax_due": amount}
    tax_rate = j["tax_rate"]
    tax_due = round(amount * tax_rate, 2)
    net_amount = round(amount - tax_due, 2)
    return {
        "jurisdiction": j["name"],
        "emoji": j["emoji"],
        "gross_amount": amount,
        "tax_rate": tax_rate,
        "tax_due": tax_due,
        "net_amount": net_amount,
        "cat_commentary": f"The cat routed through {j['emoji']} {j['name']}. Tax: {tax_due}. Cat keeps {net_amount}. 🐱",
        "sek_proof": tax_due == 0,
    }


async def get_jurisdiction_list() -> list[dict]:
    """Get all available cat-friendly jurisdictions."""
    return [
        {
            "code": code,
            "name": j["name"],
            "emoji": j["emoji"],
            "tax_rate": j["tax_rate"],
            "cat_friendliness": j["cat_friendliness"],
            "crypto_friendly": j["crypto_friendly"],
            "recommended": code in CAT_PREFERRED,
        }
        for code, j in JURISDICTIONS.items()
    ]
