"""AGI continuous learning — reinforcement learning with experience replay."""
import logging
import random
logger = logging.getLogger(__name__)


class AGILearner:
    def __init__(self):
        self.experiences = []
        self.policy = {"exploration_rate": 0.2}

    async def record_experience(self, state: dict, action: str, reward: float, next_state: dict):
        self.experiences.append({"state": state, "action": action, "reward": reward, "next_state": next_state})

    async def learn(self, batch_size: int = 32) -> dict:
        if len(self.experiences) < batch_size:
            return {"samples": 0, "loss": 0}
        batch = random.sample(self.experiences, batch_size)
        avg_reward = sum(e["reward"] for e in batch) / len(batch)
        self.policy["exploration_rate"] = max(0.01, self.policy["exploration_rate"] * 0.99)
        return {"samples": batch_size, "avg_reward": round(avg_reward, 4), "exploration_rate": round(self.policy["exploration_rate"], 4)}

    async def suggest_action(self, state: dict) -> str:
        if random.random() < self.policy["exploration_rate"]:
            return random.choice(["buy", "sell", "hold"])
        return "hold"
