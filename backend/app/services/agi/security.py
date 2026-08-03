"""AGI security — autonomous safety constraints, kill switch, self-assessment."""

import logging
from datetime import timezone, datetime
from typing import Optional

logger = logging.getLogger(__name__)


class AGISecurity:
    def __init__(self):
        self.kill_switch_engaged = False
        self.safety_score = 1.0

    async def check_safety(self, action: dict) -> dict:
        if self.kill_switch_engaged:
            return {"allowed": False, "reason": "Kill switch engaged"}
        score = 1.0
        if action.get("value", 0) > 1_000_000:
            score -= 0.2
        if action.get("leverage", 1) > 2:
            score -= 0.3
        if action.get("volatility", 0) > 0.5:
            score -= 0.1
        self.safety_score = max(0, score)
        return {"allowed": score > 0.5, "safety_score": round(score, 2), "reason": "Safety check passed" if score > 0.5 else "Safety threshold exceeded"}

    async def engage_kill_switch(self, reason: str = "Manual override") -> dict:
        self.kill_switch_engaged = True
        logger.warning("AGI kill switch engaged: %s", reason)
        return {"status": "kill_switch_engaged", "reason": reason, "timestamp": datetime.now(timezone.utc).isoformat()}

    async def disengage_kill_switch(self) -> dict:
        self.kill_switch_engaged = False
        return {"status": "kill_switch_disengaged", "timestamp": datetime.now(timezone.utc).isoformat()}

    async def self_assessment(self) -> dict:
        return {"safety_score": round(self.safety_score, 2), "kill_switch": self.kill_switch_engaged, "modules_active": 3, "recommendation": "normal_operation" if self.safety_score > 0.5 else "reduce_autonomy"}
