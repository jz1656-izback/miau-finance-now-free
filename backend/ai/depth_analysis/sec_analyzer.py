import logging
from typing import Optional

logger = logging.getLogger(__name__)

FILING_TYPES = {
    "10-K": {"name": "Annual Report", "frequency": "yearly", "sections": ["business", "risk_factors", "mdna", "financials", "controls"]},
    "10-Q": {"name": "Quarterly Report", "frequency": "quarterly", "sections": ["financials", "mdna", "risk_factors"]},
    "8-K": {"name": "Current Report", "frequency": "event-driven", "sections": ["results", "acquisitions", "management_changes", "bankruptcy"]},
    "DEF 14A": {"name": "Proxy Statement", "frequency": "yearly", "sections": ["exec_comp", "governance", "proposals"]},
}

RECENT_FILINGS = {
    "AAPL": [
        {"type": "10-K", "filed": "2025-10-31", "period": "FY2025", "size_mb": 85, "summary": "Annual report — record revenue $391B, services growth 12%"},
        {"type": "10-Q", "filed": "2026-01-31", "period": "Q1 FY2026", "size_mb": 22, "summary": "iPhone revenue $65B, Mac $8B, Services $26B"},
        {"type": "8-K", "filed": "2026-02-01", "period": "", "size_mb": 1, "summary": "Dividend increase to $0.25/share"},
    ],
    "MSFT": [
        {"type": "10-K", "filed": "2025-07-31", "period": "FY2025", "size_mb": 92, "summary": "Annual — revenue $211B, Azure growth 22%, Copilot monetization"},
        {"type": "10-Q", "filed": "2026-01-31", "period": "Q2 FY2026", "size_mb": 25, "summary": "Intelligent Cloud $21B, Office $13B, LinkedIn $4B"},
    ],
    "TSLA": [
        {"type": "10-K", "filed": "2026-01-29", "period": "FY2025", "size_mb": 78, "summary": "Annual — deliveries 1.81M, energy storage +110%, Cybertruck ramp"},
    ],
}


async def analyze_filing(ticker: str, filing_type: str = "10-K") -> dict:
    filing_info = FILING_TYPES.get(filing_type, {})
    return {
        "ticker": ticker.upper(),
        "filing_type": filing_type,
        "filing_name": filing_info.get("name", "Unknown"),
        "sections": filing_info.get("sections", []),
        "analysis": {
            "risk_assessment": _analyze_risks(ticker),
            "financial_health": _financial_health(ticker),
            "key_metrics": _key_metrics(ticker),
            "changes_from_prior": _changes_from_prior(ticker),
        },
    }


async def recent_filings(ticker: str, limit: int = 5) -> list[dict]:
    filings = RECENT_FILINGS.get(ticker.upper(), [])
    return filings[:limit]


async def search_filings(keyword: str, since: str = "2025-01-01") -> list[dict]:
    results = []
    for ticker, filings in RECENT_FILINGS.items():
        for f in filings:
            if keyword.lower() in f["summary"].lower() and f["filed"] >= since:
                results.append({"ticker": ticker, **f})
    return results[:20]


async def extract_section(ticker: str, filing_type: str, section: str) -> dict:
    filing_info = FILING_TYPES.get(filing_type, {})
    if section not in filing_info.get("sections", []):
        return {"error": f"Section '{section}' not in {filing_type}. Available: {filing_info.get('sections', [])}"}
    return {
        "ticker": ticker.upper(),
        "filing_type": filing_type,
        "section": section,
        "excerpt": f"[Simulated] Key findings from {section} section of {ticker}'s {filing_type}...",
        "key_findings": [f"Finding 1 related to {section}", f"Finding 2 related to {section}"],
    }


def _analyze_risks(ticker: str) -> dict:
    risks = {
        "AAPL": {"high": ["supply_chain", "regulatory"], "medium": ["competition", "currency"], "low": ["liquidity", "credit"]},
        "MSFT": {"high": ["regulatory", "competition"], "medium": ["cybersecurity", "integration"], "low": ["liquidity"]},
    }
    return risks.get(ticker.upper(), {"high": ["market"], "medium": ["competition"], "low": ["liquidity"]})


def _financial_health(ticker: str) -> dict:
    scores = {
        "AAPL": {"altman_z": 4.8, "current_ratio": 1.2, "debt_to_equity": 1.8, "interest_coverage": 22.0, "verdict": "healthy"},
        "MSFT": {"altman_z": 5.2, "current_ratio": 1.4, "debt_to_equity": 1.2, "interest_coverage": 28.0, "verdict": "healthy"},
        "TSLA": {"altman_z": 3.1, "current_ratio": 1.6, "debt_to_equity": 0.8, "interest_coverage": 12.0, "verdict": "stable"},
    }
    return scores.get(ticker.upper(), {"verdict": "unknown"})


def _key_metrics(ticker: str) -> dict:
    metrics = {
        "AAPL": {"revenue_b": 391, "net_income_b": 94, "fcf_b": 102, "gross_margin_pct": 43.5, "r_and_d_b": 26},
        "MSFT": {"revenue_b": 211, "net_income_b": 72, "fcf_b": 68, "gross_margin_pct": 68.9, "r_and_d_b": 24},
    }
    return metrics.get(ticker.upper(), {"revenue_b": 0})


def _changes_from_prior(ticker: str) -> dict:
    changes = {
        "AAPL": {"revenue_change_pct": 3.2, "net_income_change_pct": 5.8, "margin_change_pct": 0.5, "key_driver": "Services growth +12%"},
        "MSFT": {"revenue_change_pct": 8.5, "net_income_change_pct": 12.2, "margin_change_pct": 1.2, "key_driver": "Azure +22%, Copilot adoption"},
    }
    return changes.get(ticker.upper(), {})
