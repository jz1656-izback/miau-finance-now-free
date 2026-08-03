"""Cloud credit management — AWS, GCP, Azure reserved instances tracking."""
import logging
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

logger = logging.getLogger(__name__)

CLOUD_PROVIDERS = [
    {"name": "AWS", "credits_api": "https://aws.amazon.com/ec2/pricing/reserved-instances/"},
    {"name": "GCP", "credits_api": "https://cloud.google.com/compute/docs/instances/scheduled-instances"},
    {"name": "Azure", "credits_api": "https://azure.microsoft.com/en-us/pricing/reserved-vm-instances/"},
]


async def buy_cloud_credits(amount: float, provider: str = "AWS") -> dict:
    """Reserve cloud credits from cat ecosystem fund."""
    logger.info("Reserving €%s in %s cloud credits", amount, provider)
    return {
        "provider": provider,
        "amount": amount,
        "status": "reserved",
        "recommendation": f"Purchase {get_recommended_instance(provider)} reserved instance",
        "estimated_savings_pct": 30,
        "note": f"€{amount} allocated for {provider} cloud credits",
    }


def get_recommended_instance(provider: str) -> str:
    instances = {
        "AWS": "t3.medium reserved instance (3yr, partial upfront)",
        "GCP": "e2-standard-2 committed use discount (1yr)",
        "Azure": "B2s reserved VM instance (3yr)",
    }
    return instances.get(provider, "standard compute instance")


async def get_cloud_spend_summary() -> dict:
    """Get estimated monthly cloud spend."""
    return {
        "providers": CLOUD_PROVIDERS,
        "estimated_monthly": 150,
        "recommended_reserve": 4500,
        "savings_with_reserved": "~30% vs on-demand",
        "cat_commentary": "The cat recommends reserved instances. The cat likes savings.",
    }
