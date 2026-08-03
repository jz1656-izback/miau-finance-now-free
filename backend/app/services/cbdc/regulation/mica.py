import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


class MiCAComplianceError(Exception):
    pass


MICA_IMPLEMENTATION_DATE = datetime(2025, 6, 30, tzinfo=timezone.utc)
MICA_FULL_EFFECT_DATE = datetime(2026, 6, 30, tzinfo=timezone.utc)


@dataclass
class MiCAAssessmentResult:
    compliant: bool = True
    requirements_met: list[str] = field(default_factory=list)
    requirements_missed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    overall_score: float = 1.0


MICA_CRYPTO_ASSET_CLASSES: dict[str, dict[str, object]] = {
    "e-money_token": {
        "name": "E-Money Token (EMT)",
        "regulation": "Title II",
        "requires_whitepaper": True,
        "requires_authorization": True,
        "requires_reserve": True,
    },
    "asset_referenced_token": {
        "name": "Asset-Referenced Token (ART)",
        "regulation": "Title III",
        "requires_whitepaper": True,
        "requires_authorization": True,
        "requires_reserve": True,
        "requires_custody": True,
    },
    "utility_token": {
        "name": "Utility Token",
        "regulation": "Title IV",
        "requires_whitepaper": False,
        "requires_authorization": False,
        "requires_reserve": False,
    },
    "cbdc": {
        "name": "Central Bank Digital Currency",
        "regulation": "Exempt (Central Bank)",
        "requires_whitepaper": False,
        "requires_authorization": False,
        "requires_reserve": False,
    },
}


def classify_crypto_asset(token_type: str, is_cbdc_issued: bool = False) -> dict:
    if is_cbdc_issued:
        return dict(MICA_CRYPTO_ASSET_CLASSES["cbdc"])
    cls = MICA_CRYPTO_ASSET_CLASSES.get(token_type)
    if not cls:
        raise MiCAComplianceError(f"Unknown crypto asset class: {token_type}")
    return dict(cls)


def check_whitepaper_requirements(token_type: str, has_whitepaper: bool = False) -> bool:
    cls = classify_crypto_asset(token_type)
    if cls.get("requires_whitepaper") and not has_whitepaper:
        return False
    return True


def check_authorization_requirements(token_type: str, is_authorized: bool = False) -> bool:
    cls = classify_crypto_asset(token_type)
    if cls.get("requires_authorization") and not is_authorized:
        return False
    return True


def check_reserve_requirements(token_type: str, has_reserve: bool = False) -> bool:
    cls = classify_crypto_asset(token_type)
    if cls.get("requires_reserve") and not has_reserve:
        return False
    return True


def assess_mica_compliance(
    token_type: str,
    is_cbdc_issued: bool = False,
    has_whitepaper: bool = False,
    is_authorized: bool = False,
    has_reserve: bool = False,
    has_custody: bool = False,
    is_marketing_to_eu: bool = False,
    has_aml_procedures: bool = False,
    transaction_volume_eur: float = 0.0,
) -> MiCAAssessmentResult:
    result = MiCAAssessmentResult()

    cls = classify_crypto_asset(token_type, is_cbdc_issued)

    if cls.get("requires_whitepaper"):
        if has_whitepaper:
            result.requirements_met.append("Crypto-asset whitepaper published")
        else:
            result.requirements_missed.append("Crypto-asset whitepaper required (Art. 6)")
            result.compliant = False

    if cls.get("requires_authorization"):
        if is_authorized:
            result.requirements_met.append("Authorization obtained from competent authority")
        else:
            result.requirements_missed.append("Authorization required (Art. 16)")
            result.compliant = False

    if cls.get("requires_reserve"):
        if has_reserve:
            result.requirements_met.append("Reserve assets maintained (Art. 36)")
        else:
            result.requirements_missed.append("Reserve assets required (Art. 36)")
            result.compliant = False

    if cls.get("requires_custody") and not has_custody:
        result.requirements_missed.append("Custody arrangements required (Art. 37)")
        result.compliant = False

    if is_marketing_to_eu:
        if has_whitepaper:
            result.requirements_met.append("Marketing communications comply with Art. 29")
        else:
            result.warnings.append("Marketing to EU without approved whitepaper — potential Art. 29 violation")

    if not has_aml_procedures:
        result.warnings.append("AML/CFT procedures recommended (5AMLD/MiCA Art. 62)")

    if transaction_volume_eur > 1_000_000:
        result.warnings.append(f"High transaction volume (€{transaction_volume_eur:,.2f}) — enhanced monitoring recommended")

    met = len(result.requirements_met)
    missed = len(result.requirements_missed)
    warnings = len(result.warnings)
    total = met + missed

    result.overall_score = round(met / total, 2) if total > 0 else 1.0
    return result


def get_mica_regulatory_status() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "regulation": "Markets in Crypto-Assets (MiCA)",
        "jurisdiction": "European Union",
        "implementation_date": MICA_IMPLEMENTATION_DATE.isoformat(),
        "full_effect_date": MICA_FULL_EFFECT_DATE.isoformat(),
        "status": "in_effect" if now >= MICA_IMPLEMENTATION_DATE else "pending",
        "phases": {
            "stablecoins_emts_arts": "June 30, 2025",
            "full_regime": "June 30, 2026",
        },
    }
