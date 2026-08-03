"""AGI compliance — hard guardrails, regulatory rules, audit trail for autonomous decisions."""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

_MAX_DAILY_LOSS_PCT = 5.0
_MAX_POSITION_PCT = 25.0
_RESTRICTED_TICKERS = ["PENNY", "OTC", "CRYPTO_MEME"]
_MIN_HOLDING_DAYS = 1
_MAX_DAILY_TRADES = 50


@dataclass
class ComplianceCheck:
    passed: bool
    rule: str
    detail: str = ""
    severity: str = "info"

    def to_dict(self) -> dict[str, Any]:
        return {"rule": self.rule, "passed": self.passed, "detail": self.detail, "severity": self.severity}


async def check_trade(
    ticker: str,
    side: str,
    qty: float,
    price: float,
    portfolio_value: float,
    daily_loss: float = 0.0,
    daily_trades: int = 0,
) -> dict[str, Any]:
    checks: list[ComplianceCheck] = []
    trade_value = qty * price

    if trade_value > portfolio_value:
        checks.append(ComplianceCheck(False, "sufficient_funds", f"Trade ${trade_value:.2f} > portfolio ${portfolio_value:.2f}", "critical"))

    pos_pct = trade_value / portfolio_value * 100 if portfolio_value > 0 else 0
    if pos_pct > _MAX_POSITION_PCT:
        checks.append(ComplianceCheck(False, "position_size", f"Position would be {pos_pct:.1f}% (max {_MAX_POSITION_PCT}%)", "high"))

    for restricted in _RESTRICTED_TICKERS:
        if restricted in ticker.upper():
            checks.append(ComplianceCheck(False, "restricted_ticker", f"{ticker} is restricted", "critical"))
            break

    if daily_loss > _MAX_DAILY_LOSS_PCT:
        checks.append(ComplianceCheck(False, "daily_loss_limit", f"Daily loss {daily_loss:.1f}% > {_MAX_DAILY_LOSS_PCT}%", "critical"))

    if daily_trades >= _MAX_DAILY_TRADES:
        checks.append(ComplianceCheck(False, "daily_trade_limit", f"Daily trades {daily_trades} >= {_MAX_DAILY_TRADES}", "high"))

    all_passed = all(c.passed for c in checks)
    return {
        "ticker": ticker,
        "side": side,
        "trade_value": round(trade_value, 2),
        "compliant": all_passed,
        "checks": [c.to_dict() for c in checks],
        "critical_violations": sum(1 for c in checks if not c.passed and c.severity == "critical"),
        "high_violations": sum(1 for c in checks if not c.passed and c.severity == "high"),
        "decision": "ALLOWED" if all_passed else "BLOCKED",
    }


async def get_audit_trail(
    limit: int = 50,
    status_filter: Optional[str] = None,
) -> list[dict[str, Any]]:
    return []


async def log_compliance_event(event: dict[str, Any]) -> None:
    logger.info("Compliance: %s", event)
