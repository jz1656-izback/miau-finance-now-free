"""Community strategy audit — code review, risk scoring, compliance check."""

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

RISKY_PATTERNS = [
    (r"os\.system\(|subprocess\.", "shell_execution", 90),
    (r"__import__|eval\(|exec\(|compile\(|getattr\(.*__", "dynamic_code", 85),
    (r"while\s+True:|while\s+1:", "infinite_loop_risk", 70),
    (r"open\(.*['\"]w['\"]\)|open\(.*['\"]a['\"]\)", "file_write", 60),
    (r"requests\.(get|post)\(.*timeout", "missing_timeout", 50),
    (r"\.delete\(|\.drop\(|\.truncate\(", "destructive_db", 95),
]


async def audit_code(code: str) -> dict:
    issues = []
    score = 100
    for pattern, category, penalty in RISKY_PATTERNS:
        if re.search(pattern, code):
            issues.append({"category": category, "severity": penalty, "pattern": pattern})
            score -= penalty * 0.5
    return {
        "audit_score": round(max(0, score), 1),
        "risk_level": "low" if score > 80 else "medium" if score > 50 else "high",
        "issues_found": len(issues),
        "issues": issues,
        "lines_of_code": len(code.splitlines()),
    }


async def validate_strategy(code: str, expected_entry_points: Optional[list[str]] = None) -> dict:
    audit = await audit_code(code)
    entry_points = expected_entry_points or ["generate_signals", "should_buy", "should_sell"]
    found = [ep for ep in entry_points if ep in code]
    return {
        "passed": audit["risk_level"] != "high" and len(found) == len(entry_points),
        "audit": audit,
        "entry_points_found": found,
        "entry_points_missing": [ep for ep in entry_points if ep not in found],
    }
