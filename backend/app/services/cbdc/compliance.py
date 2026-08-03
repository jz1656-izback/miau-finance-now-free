import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


class CBDCComplianceError(Exception):
    pass


@dataclass
class CBDCTransactionCheck:
    passed: bool = True
    flags: list[str] = field(default_factory=list)
    risk_score: float = 0.0


RESTRICTED_JURISDICTIONS: list[str] = [
    "IR", "KP", "CU", "SY", "RU", "BY",  # OFAC-sanctioned
]

DAILY_TRANSACTION_LIMITS: dict[str, float] = {
    "retail": 10_000.0,
    "wholesale": 1_000_000.0,
    "interbank": 50_000_000.0,
}

TRAVEL_RULE_THRESHOLD = 1_000.0  # EUR/USD equivalent


@dataclass
class CBDCJurisdictionRules:
    jurisdiction: str
    kyc_required: bool = True
    aml_required: bool = True
    travel_rule_threshold: float = TRAVEL_RULE_THRESHOLD
    daily_transaction_limit: float = DAILY_TRANSACTION_LIMITS["retail"]
    requires_tax_reporting: bool = True
    sanctions_screening: bool = True
    transaction_monitoring: bool = True
    cbdc_type: str = "retail"  # retail, wholesale, interbank


JURISDICTION_RULES: dict[str, CBDCJurisdictionRules] = {
    "EU": CBDCJurisdictionRules(jurisdiction="EU", cbdc_type="retail", daily_transaction_limit=DAILY_TRANSACTION_LIMITS["retail"]),
    "CN": CBDCJurisdictionRules(jurisdiction="CN", cbdc_type="retail", requires_tax_reporting=False),
    "US": CBDCJurisdictionRules(jurisdiction="US", cbdc_type="wholesale", daily_transaction_limit=DAILY_TRANSACTION_LIMITS["wholesale"]),
    "JP": CBDCJurisdictionRules(jurisdiction="JP", cbdc_type="retail"),
    "GB": CBDCJurisdictionRules(jurisdiction="GB", cbdc_type="retail"),
}


def check_jurisdiction_restrictions(country_code: str) -> CBDCTransactionCheck:
    check = CBDCTransactionCheck()
    if country_code.upper() in RESTRICTED_JURISDICTIONS:
        check.passed = False
        check.flags.append(f"Jurisdiction {country_code} is restricted under sanctions")
        check.risk_score = 1.0
    return check


def check_daily_limits(amount: float, cbdc_type: str = "retail") -> CBDCTransactionCheck:
    check = CBDCTransactionCheck()
    limit = DAILY_TRANSACTION_LIMITS.get(cbdc_type, DAILY_TRANSACTION_LIMITS["retail"])
    if amount > limit:
        check.passed = False
        check.flags.append(f"Amount ${amount:,.2f} exceeds daily limit of ${limit:,.2f} for {cbdc_type}")
        check.risk_score = min(1.0, amount / limit * 0.5)
    return check


def check_travel_rule(amount: float, origin_jurisdiction: str, destination_jurisdiction: str) -> CBDCTransactionCheck:
    check = CBDCTransactionCheck()
    if amount >= TRAVEL_RULE_THRESHOLD and origin_jurisdiction != destination_jurisdiction:
        check.flags.append(f"Travel Rule applies: ${amount:,.2f} cross-border transfer "
                          f"from {origin_jurisdiction} to {destination_jurisdiction}")
        check.risk_score = 0.3
    return check


def check_sanctions(sender_country: str, recipient_country: str) -> CBDCTransactionCheck:
    check = CBDCTransactionCheck()
    if sender_country.upper() in RESTRICTED_JURISDICTIONS:
        check.passed = False
        check.flags.append(f"Sender jurisdiction {sender_country} is sanctioned")
        check.risk_score = 1.0
    if recipient_country.upper() in RESTRICTED_JURISDICTIONS:
        check.passed = False
        check.flags.append(f"Recipient jurisdiction {recipient_country} is sanctioned")
        check.risk_score = 1.0
    return check


def assess_transaction_risk(
    amount: float,
    sender_jurisdiction: str,
    recipient_jurisdiction: str,
    cbdc_type: str = "retail",
    is_cross_border: bool = False,
    is_high_value: bool = False,
    is_structured: bool = False,
) -> CBDCTransactionCheck:
    checks: list[CBDCTransactionCheck] = []
    checks.append(check_jurisdiction_restrictions(sender_jurisdiction))
    checks.append(check_jurisdiction_restrictions(recipient_jurisdiction))
    checks.append(check_daily_limits(amount, cbdc_type))
    checks.append(check_sanctions(sender_jurisdiction, recipient_jurisdiction))

    if is_cross_border:
        checks.append(check_travel_rule(amount, sender_jurisdiction, recipient_jurisdiction))

    combined = CBDCTransactionCheck()
    for c in checks:
        if not c.passed:
            combined.passed = False
        combined.flags.extend(c.flags)
        combined.risk_score = max(combined.risk_score, c.risk_score)

    if is_high_value:
        combined.flags.append("High-value transaction flagged for manual review")
        combined.risk_score = max(combined.risk_score, 0.6)
    if is_structured:
        combined.flags.append("Structured transaction pattern detected — potential structuring")
        combined.risk_score = max(combined.risk_score, 0.8)

    combined.risk_score = round(min(1.0, combined.risk_score), 2)
    return combined


def get_risk_level(score: float) -> str:
    if score >= 0.8:
        return "CRITICAL"
    elif score >= 0.5:
        return "HIGH"
    elif score >= 0.2:
        return "MEDIUM"
    else:
        return "LOW"


def format_compliance_report(
    transaction_id: str,
    amount: float,
    currency: str,
    sender: str,
    recipient: str,
    assessment: CBDCTransactionCheck,
) -> dict:
    return {
        "transaction_id": transaction_id,
        "amount": amount,
        "currency": currency,
        "sender": sender,
        "recipient": recipient,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "compliance_check": assessment.passed,
        "risk_score": assessment.risk_score,
        "risk_level": get_risk_level(assessment.risk_score),
        "flags": assessment.flags,
        "requires_manual_review": assessment.risk_score >= 0.5,
    }
