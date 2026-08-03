import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


class FundComplianceError(Exception):
    pass


@dataclass
class InvestorProfile:
    income_annual: float = 0.0
    net_worth: float = 0.0
    investment_experience_years: int = 0
    is_entity: bool = False
    entity_assets: float = 0.0
    jurisdiction: str = "US"

    def is_accredited(self) -> bool:
        if self.is_entity:
            return self.entity_assets >= 5_000_000
        return (
            self.income_annual >= 200_000
            and self.net_worth >= 1_000_000
        )


REGULATION_D_THRESHOLDS = {
    "income_individual": 200_000,
    "income_joint": 300_000,
    "net_worth": 1_000_000,
    "entity_assets": 5_000_000,
}

SEC_REGULATION_OFFERINGS = {
    "506b": {
        "name": "Rule 506(b)",
        "max_investors": 35,
        "general_solicitation": False,
        "requires_accredited": True,
    },
    "506c": {
        "name": "Rule 506(c)",
        "max_investors": None,
        "general_solicitation": True,
        "requires_accredited": True,
    },
}


@dataclass
class FundComplianceResult:
    accredited: bool = False
    eligibility_flags: list[str] = field(default_factory=list)
    max_allocation: float = 0.0
    jurisdiction_ok: bool = True
    kyc_required: bool = True
    risk_level: str = "MODERATE"


ACCREDITATION_TIERS = {
    "individual": {
        "income_threshold": 200_000,
        "net_worth_threshold": 1_000_000,
        "max_allocation_pct": 0.10,
    },
    "joint": {
        "income_threshold": 300_000,
        "net_worth_threshold": 1_000_000,
        "max_allocation_pct": 0.15,
    },
    "entity": {
        "assets_threshold": 5_000_000,
        "max_allocation_pct": 0.20,
    },
    "qualified_purchaser": {
        "investments_threshold": 5_000_000,
        "max_allocation_pct": 0.30,
    },
}


def check_accredited_individual(income_annual: float, net_worth: float, investment_experience_years: int) -> FundComplianceResult:
    result = FundComplianceResult()
    flags = []

    if income_annual >= 200_000:
        flags.append(f"Income ${income_annual:,.2f} meets individual threshold ($200K)")
    else:
        flags.append(f"Income ${income_annual:,.2f} below individual threshold ($200K)")

    if net_worth >= 1_000_000:
        flags.append(f"Net worth ${net_worth:,.2f} meets threshold ($1M)")
    else:
        flags.append(f"Net worth ${net_worth:,.2f} below threshold ($1M)")

    if investment_experience_years < 2:
        flags.append(f"Limited investment experience ({investment_experience_years} years) — suitability review recommended")

    accredited = income_annual >= 200_000 and net_worth >= 1_000_000
    result.accredited = accredited
    result.eligibility_flags = flags
    result.max_allocation = net_worth * 0.10 if accredited else 0

    if income_annual >= 1_000_000:
        result.risk_level = "LOW"
    elif net_worth >= 5_000_000:
        result.risk_level = "LOW"
    elif accredited:
        result.risk_level = "MODERATE"
    else:
        result.risk_level = "HIGH"

    return result


def check_accredited_joint(income_joint: float, net_worth: float) -> FundComplianceResult:
    result = FundComplianceResult()
    accredited = income_joint >= 300_000 and net_worth >= 1_000_000
    result.accredited = accredited
    result.max_allocation = net_worth * 0.15 if accredited else 0
    return result


def check_accredited_entity(assets: float) -> FundComplianceResult:
    result = FundComplianceResult()
    accredited = assets >= 5_000_000
    result.accredited = accredited
    result.max_allocation = assets * 0.20 if accredited else 0
    return result


def check_qualified_purchaser(investments: float) -> FundComplianceResult:
    result = FundComplianceResult()
    qualified = investments >= 5_000_000
    result.accredited = qualified
    result.max_allocation = investments * 0.30 if qualified else 0
    return result


def check_regulatory_offering(profile: InvestorProfile, offering_type: str = "506b") -> FundComplianceResult:
    result = check_accredited_individual(profile.income_annual, profile.net_worth, profile.investment_experience_years)
    offering = SEC_REGULATION_OFFERINGS.get(offering_type)

    if not profile.is_entity and offering:
        if offering["requires_accredited"] and not result.accredited:
            result.eligibility_flags.append(f"Accredited investor required for {offering['name']}")
            result.risk_level = "BLOCKED"

        if offering.get("general_solicitation"):
            result.eligibility_flags.append("General solicitation permitted under Rule 506(c) — verification required")

    if profile.jurisdiction.upper() not in ("US", ""):
        result.jurisdiction_ok = False
        result.eligibility_flags.append(f"Non-US jurisdiction ({profile.jurisdiction}) — Regulation S may apply")

    return result


def verify_investor_suitability(
    profile: InvestorProfile,
    requested_allocation: float,
) -> FundComplianceResult:
    result = check_accredited_individual(profile.income_annual, profile.net_worth, profile.investment_experience_years)

    if not result.accredited:
        result.eligibility_flags.append("Investor is not accredited — fund access restricted")

    if result.max_allocation > 0 and requested_allocation > result.max_allocation:
        result.eligibility_flags.append(
            f"Requested ${requested_allocation:,.2f} exceeds max allocation "
            f"${result.max_allocation:,.2f} ({result.max_allocation/requested_allocation*100:.0f}% of net worth)"
        )

    if profile.investment_experience_years < 1:
        result.eligibility_flags.append("No investment experience — mandatory educational review")

    if profile.jurisdiction.upper() not in ("US", "EU", "GB", "CA", "AU", "SG", "HK", "JP", ""):
        result.eligibility_flags.append(f"Jurisdiction {profile.jurisdiction} requires local compliance review")

    return result


SUPPORTED_JURISDICTIONS = {
    "US": "SEC Regulation D / Accredited Investor",
    "EU": "AIFMD / Professional Investor",
    "GB": "FCA / Certified High Net Worth",
    "CA": "NI 45-106 / Accredited Investor",
    "AU": "Corporations Act / Wholesale Investor",
    "SG": "SFA / Accredited Investor",
    "HK": "SFO / Professional Investor",
    "JP": "FIEA / Qualified Institutional Investor",
}


def get_jurisdiction_rules(jurisdiction: str) -> Optional[dict]:
    rules = SUPPORTED_JURISDICTIONS.get(jurisdiction.upper())
    if not rules:
        return None
    return {
        "jurisdiction": jurisdiction.upper(),
        "framework": rules,
        "requires_kyc": True,
        "requires_suitability": True,
        "max_leverage": 2.0 if jurisdiction.upper() == "US" else 5.0,
    }
