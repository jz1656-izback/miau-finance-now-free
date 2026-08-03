"""AGI governance — oversight framework, decision logging, human-in-the-loop."""

import logging
from datetime import timezone, datetime
from typing import Optional

logger = logging.getLogger(__name__)


class AGIGovernance:
    def __init__(self):
        self.decisions: list[dict] = []
        self.human_approval_required = True

    async def review_decision(self, decision: dict) -> dict:
        requires_approval = decision.get("value", 0) > 100000 or decision.get("type") in ("strategy_change", "risk_limit_change")
        return {"requires_human_approval": requires_approval, "decision_id": f"dec_{len(self.decisions) + 1}", "risk_level": "high" if requires_approval else "low"}

    async def approve_decision(self, decision_id: str, approved_by: str) -> dict:
        return {"decision_id": decision_id, "approved_by": approved_by, "approved_at": datetime.now(timezone.utc).isoformat(), "status": "approved"}

    async def log_decision(self, decision: dict, outcome: str) -> dict:
        entry = {"timestamp": datetime.now(timezone.utc).isoformat(), **decision, "outcome": outcome}
        self.decisions.append(entry)
        return entry

    async def get_oversight_summary(self) -> dict:
        return {"total_decisions": len(self.decisions), "approved": sum(1 for d in self.decisions if d.get("outcome") == "approved"), "rejected": sum(1 for d in self.decisions if d.get("outcome") == "rejected")}
