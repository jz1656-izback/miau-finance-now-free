"""Strategy licensing — rent/buy strategies, revenue sharing, subscription tiers."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

_licenses: dict[str, dict] = {}

LICENSE_TIERS = {
    "free": {"price": 0, "duration_days": 7, "features": ["view_code", "paper_trade"]},
    "standard": {"price": 50, "duration_days": 30, "features": ["view_code", "paper_trade", "live_trade", "modify_params"]},
    "premium": {"price": 200, "duration_days": 90, "features": ["view_code", "paper_trade", "live_trade", "modify_params", "commercial_use", "support"]},
    "revenue_share": {"price": 0, "revenue_share_pct": 20, "duration_days": 365, "features": ["view_code", "live_trade", "modify_params", "commercial_use"]},
}

REVENUE_SHARE_PCT = 20


async def purchase_license(buyer: str, strategy_id: str, tier: str) -> Optional[dict]:
    if tier not in LICENSE_TIERS:
        return None
    config = LICENSE_TIERS[tier]
    license_id = f"lic_{strategy_id[:4]}_{buyer[:4]}"
    license_data = {
        "id": license_id,
        "buyer": buyer,
        "strategy_id": strategy_id,
        "tier": tier,
        "price": config["price"],
        "features": config["features"],
        "purchased_at": __import__("datetime").datetime.now(timezone.utc).isoformat(),
    }
    if "revenue_share_pct" in config:
        license_data["revenue_share_pct"] = config["revenue_share_pct"]
    _licenses[license_id] = license_data
    return license_data


async def get_license(license_id: str) -> Optional[dict]:
    return _licenses.get(license_id)


async def list_licenses(buyer: str) -> list[dict]:
    return [l for l in _licenses.values() if l.get("buyer") == buyer]
