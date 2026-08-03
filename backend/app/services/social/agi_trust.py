"""AGI social trust — community reputation, trust scoring for autonomous agents."""
import logging
from typing import Optional
logger = logging.getLogger(__name__)


class AGITrust:
    def __init__(self):
        self.trust_scores = {}

    async def score_trust(self, agent_id: str, accuracy: float, consistency: float, votes: int) -> float:
        score = accuracy * 0.4 + consistency * 0.3 + min(votes / 100, 1) * 0.3
        self.trust_scores[agent_id] = round(score * 100, 1)
        return self.trust_scores[agent_id]

    async def get_trust(self, agent_id: str) -> Optional[dict]:
        score = self.trust_scores.get(agent_id)
        if score is None:
            return None
        return {"agent_id": agent_id, "trust_score": score, "level": "high" if score > 80 else "medium" if score > 50 else "low"}
