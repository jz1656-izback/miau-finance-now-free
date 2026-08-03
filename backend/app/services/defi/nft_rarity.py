"""NFT rarity scoring — trait-based rarity, collection ranking, statistical scoring."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

TRAIT_RARITY: dict[str, dict[str, float]] = {
    "background": {"Blue": 0.35, "Red": 0.15, "Gold": 0.05, "Purple": 0.10, "Green": 0.20, "Black": 0.15},
    "fur": {"Brown": 0.30, "Black": 0.20, "White": 0.15, "Gold": 0.05, "Pink": 0.08, "Robot": 0.02},
    "eyes": {"Blue": 0.25, "Red": 0.20, "Green": 0.15, "Laser": 0.03, "Heart": 0.02, "Zombie": 0.05},
    "hat": {"None": 0.40, "Beanie": 0.15, "Top Hat": 0.08, "Crown": 0.03, "Cap": 0.12, "Headband": 0.10},
    "mouth": {"Smile": 0.30, "Frown": 0.20, "Open": 0.15, "Gold Grill": 0.03, "Tongue": 0.05, "Mask": 0.08},
}

RARITY_LABELS = [
    (0.001, "Mythic"), (0.01, "Legendary"), (0.05, "Epic"),
    (0.10, "Rare"), (0.25, "Uncommon"), (1.0, "Common"),
]


def calculate_trait_rarity(traits: dict[str, str]) -> dict:
    """Calculate rarity score for an NFT based on its traits."""
    score = 1.0
    details = []
    for category, trait in traits.items():
        trait_dist = TRAIT_RARITY.get(category, {})
        probability = trait_dist.get(trait, 0.5)
        rarity = 1 / probability if probability > 0 else 2
        score *= rarity
        details.append({"trait": trait, "category": category, "probability": probability, "rarity_factor": round(rarity, 2)})
    return {"rarity_score": round(score, 2), "details": details}


def get_rarity_label(score: float) -> str:
    for threshold, label in RARITY_LABELS:
        if score <= 1 / threshold:
            return label
    return "Common"


def rank_in_collection(nft_score: float, collection_scores: list[float]) -> dict:
    sorted_scores = sorted(collection_scores, reverse=True)
    rank = sum(1 for s in sorted_scores if s > nft_score) + 1
    total = len(sorted_scores)
    percentile = round((1 - rank / total) * 100, 1) if total > 0 else 0
    return {"rank": rank, "total": total, "percentile": percentile, "label": get_rarity_label(nft_score)}


def estimate_collection_stats(collection_size: int = 10000) -> dict:
    import random
    scores = [random.gauss(100, 50) for _ in range(min(collection_size, 1000))]
    avg_score = sum(scores) / len(scores) if scores else 0
    return {"avg_rarity_score": round(avg_score, 2), "mythic_count": sum(1 for s in scores if s > 1000)}
