"""Strategy reputation system — ratings, reviews, performance verification."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

_ratings: dict[str, list[dict]] = {}
_reviews: dict[str, list[dict]] = {}


async def rate_strategy(strategy_id: str, user: str, rating: int, review: str = "") -> dict:
    rating = max(1, min(5, rating))
    if strategy_id not in _ratings:
        _ratings[strategy_id] = []
    entry = {"user": user, "rating": rating, "review": review, "created_at": __import__("datetime").datetime.now(timezone.utc).isoformat()}
    _ratings[strategy_id].append(entry)
    avg = sum(r["rating"] for r in _ratings[strategy_id]) / len(_ratings[strategy_id])
    return {"strategy_id": strategy_id, "user_rating": rating, "average_rating": round(avg, 2), "total_ratings": len(_ratings[strategy_id])}


async def get_strategy_reputation(strategy_id: str) -> dict:
    ratings = _ratings.get(strategy_id, [])
    avg = sum(r["rating"] for r in ratings) / len(ratings) if ratings else 0
    distribution = {i: sum(1 for r in ratings if r["rating"] == i) for i in range(1, 6)}
    return {"strategy_id": strategy_id, "average_rating": round(avg, 2), "total_ratings": len(ratings), "distribution": distribution, "reviews": ratings[-5:]}


async def get_user_reputation(user: str) -> dict:
    authored = sum(1 for r in _ratings.values() for e in r if e.get("user") == user)
    return {"user": user, "total_reviews": authored, "trust_score": min(100, authored * 10)}
