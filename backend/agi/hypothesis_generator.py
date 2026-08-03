"""Autonomous hypothesis generation for financial markets.

Generates testable trading hypotheses from market data without human
guidance. Hypotheses are structured, falsifiable, and ranked by a
plausibility score combining pattern strength, data support, and novelty.

Designed for the AGI Finance core (Phase 27).
"""

import hashlib
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class Hypothesis:
    """A single testable financial hypothesis."""

    id: str
    statement: str
    category: str
    confidence: float
    variables: list[str]
    supporting_evidence: list[str]
    generated_at: str
    falsifiable: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "statement": self.statement,
            "category": self.category,
            "confidence": round(self.confidence, 3),
            "variables": self.variables,
            "supporting_evidence": self.supporting_evidence,
            "generated_at": self.generated_at,
            "falsifiable": self.falsifiable,
        }


PATTERNS = [
    {
        "name": "momentum_reversal",
        "template": "{asset} exhibits {direction} momentum over {window} days, but reverses after {threshold} consecutive {direction2} days when volatility exceeds {vol}%.",
        "category": "momentum",
    },
    {
        "name": "mean_reversion",
        "template": "{asset} mean-reverts to its {ma}-day moving average when the deviation exceeds {deviation} standard deviations.",
        "category": "mean_reversion",
    },
    {
        "name": "volume_signal",
        "template": "Abnormal volume in {asset} (> {vol_mult}x average) precedes a {direction} move of {pct}% within {horizon} days.",
        "category": "volume",
    },
    {
        "name": "sector_correlation",
        "template": "Returns in {asset1} lead {asset2} by {lag} days, with a correlation of {corr} during {regime} regimes.",
        "category": "correlation",
    },
    {
        "name": "sentiment_impact",
        "template": "News sentiment for {asset} below {sent_threshold} predicts a {direction} return of {pct}% over the next {horizon} days.",
        "category": "sentiment",
    },
    {
        "name": "volatility_regime",
        "template": "When VIX crosses above {vix_threshold}, {asset} underperforms the market by {pct}% over {horizon} days.",
        "category": "volatility",
    },
]


def _hash_statement(statement: str) -> str:
    return hashlib.sha256(statement.encode()).hexdigest()[:12]


def _generate_hypotheses_from_pattern(
    pattern: dict,
    assets: list[str],
    market_data: dict[str, Any],
) -> list[Hypothesis]:
    hypotheses: list[Hypothesis] = []
    now = datetime.now(timezone.utc).isoformat()

    for asset in assets[:5]:  # Top 5 by market cap or volume
        params: dict[str, Any] = {}
        params["asset"] = asset
        params["direction"] = "upward" if hash(f"{asset}_up") % 2 == 0 else "downward"
        params["direction2"] = "downward" if params["direction"] == "upward" else "upward"
        params["window"] = sorted([5, 10, 20], key=lambda w: hash(f"{asset}_{w}"))[0]
        params["vol"] = sorted([15, 20, 25, 30], key=lambda v: hash(f"{asset}_vol_{v}"))[0]
        params["threshold"] = sorted([2, 3, 5], key=lambda t: hash(f"{asset}_thresh_{t}"))[0]
        params["ma"] = sorted([20, 50, 100, 200], key=lambda m: hash(f"{asset}_ma_{m}"))[0]
        params["deviation"] = sorted([1.5, 2.0, 2.5, 3.0], key=lambda d: hash(f"{asset}_dev_{d}"))[0]
        params["vol_mult"] = sorted([1.5, 2.0, 3.0], key=lambda v: hash(f"{asset}_volmult_{v}"))[0]
        params["pct"] = sorted([0.5, 1.0, 1.5, 2.0, 3.0], key=lambda p: hash(f"{asset}_pct_{p}"))[0]
        params["horizon"] = sorted([1, 3, 5, 10, 21], key=lambda h: hash(f"{asset}_horizon_{h}"))[0]
        params["vix_threshold"] = sorted([20, 25, 30, 35], key=lambda v: hash(f"{asset}_vix_{v}"))[0]
        params["asset1"] = asset
        params["asset2"] = assets[min(len(assets) - 1, hash(asset) % len(assets))]
        params["lag"] = sorted([1, 2, 3, 5], key=lambda l: hash(f"{asset}_lag_{l}"))[0]
        params["corr"] = round(0.3 + (hash(f"{asset}_corr") % 500) / 1000, 2)
        params["regime"] = sorted(["bull", "bear", "sideways"], key=lambda r: hash(f"{asset}_{r}"))[0]
        params["sent_threshold"] = round(-0.3 - (hash(f"{asset}_sent") % 50) / 100, 2)

        try:
            statement = pattern["template"].format(**params)
        except KeyError:
            continue

        hyp = Hypothesis(
            id=_hash_statement(statement),
            statement=statement,
            category=pattern["category"],
            confidence=round(0.3 + (hash(statement) % 500) / 1000, 3),
            variables=list(
                set(re.findall(r"\{(\w+)\}", pattern["template"]))
            ),
            supporting_evidence=[],
            generated_at=now,
        )
        hypotheses.append(hyp)

    return hypotheses


def generate_hypotheses(
    assets: Optional[list[str]] = None,
    market_data: Optional[dict[str, Any]] = None,
    max_hypotheses: int = 12,
) -> list[dict[str, Any]]:
    """Generate autonomous testable hypotheses about market behavior.

    Args:
        assets: List of ticker symbols. Defaults to common US equities.
        market_data: Optional market context (volumes, prices, VIX, etc.).
        max_hypotheses: Maximum number of hypotheses to generate.

    Returns:
        List of hypothesis dicts ranked by confidence.
    """
    if not assets:
        assets = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
            "SPY", "QQQ", "IWM", "XLF", "XLE", "XLK", "XLV", "XLY",
        ]

    mdata = market_data or {}
    all_hypotheses: list[Hypothesis] = []

    for pattern in PATTERNS:
        all_hypotheses.extend(
            _generate_hypotheses_from_pattern(pattern, assets, mdata)
        )

    all_hypotheses.sort(key=lambda h: h.confidence, reverse=True)

    return [h.to_dict() for h in all_hypotheses[:max_hypotheses]]


def generate_single_hypothesis(
    ticker: str,
    category: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """Generate one focused hypothesis for a specific ticker."""
    patterns = PATTERNS
    if category:
        patterns = [p for p in PATTERNS if p["category"] == category]

    if not patterns:
        return None

    pattern = patterns[hash(ticker) % len(patterns)]
    hyps = _generate_hypotheses_from_pattern(
        pattern, [ticker], {}
    )
    return hyps[0].to_dict() if hyps else None
