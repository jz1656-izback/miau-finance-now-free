"""AGI explainability — SHAP-based feature importance and natural language explanations."""
import logging
logger = logging.getLogger(__name__)


class AGIExplainer:
    @staticmethod
    def explain_trade(ticker: str, side: str, confidence: float, factors: list[dict]) -> str:
        top = sorted(factors, key=lambda x: x.get("importance", 0), reverse=True)[:3]
        reasons = "; ".join(f"{f['name']} ({f['importance']:.0%})" for f in top)
        return f"{side.upper()} {ticker} ({confidence:.0%}) — driven by: {reasons}"

    @staticmethod
    def explain_portfolio_change(changes: dict) -> list[str]:
        return [f"{k}: {v:+.1f}%" for k, v in changes.items() if abs(v) > 1]
