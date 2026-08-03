import json
import logging
import re
from dataclasses import dataclass, asdict
from typing import Optional

from app.config import settings
from app.services.ai.client import AIClient
from app.services.ai.advisor import sanitize_prompt
from app.services.ai.prompts.nlq import PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

INTENT_MAP = {
    "price": {"endpoint": "/api/v1/market/live", "method": "GET"},
    "live_price": {"endpoint": "/api/v1/market/live", "method": "GET"},
    "historical": {"endpoint": "/api/v1/market/historical/{ticker}", "method": "GET"},
    "portfolio": {"endpoint": "/api/v1/portfolios", "method": "GET"},
    "portfolio_detail": {"endpoint": "/api/v1/portfolios/{id}", "method": "GET"},
    "positions": {"endpoint": "/api/v1/portfolios/{id}/positions", "method": "GET"},
    "analytics": {"endpoint": "/api/v1/analytics/summary", "method": "GET"},
    "news": {"endpoint": "/api/v1/news/market", "method": "GET"},
    "company_news": {"endpoint": "/api/v1/news/company/{ticker}", "method": "GET"},
    "fundamentals": {"endpoint": "/api/v1/fundamentals/{ticker}", "method": "GET"},
    "earnings": {"endpoint": "/api/v1/fundamentals/{ticker}/earnings", "method": "GET"},
    "watchlist": {"endpoint": "/api/v1/watchlist/items", "method": "GET"},
    "options": {"endpoint": "/api/v1/options/{ticker}", "method": "GET"},
    "sectors": {"endpoint": "/api/v1/market/sectors", "method": "GET"},
    "movers": {"endpoint": "/api/v1/market/movers", "method": "GET"},
    "indicators": {"endpoint": "/api/v1/market/indicators", "method": "GET"},
    "signals": {"endpoint": "/api/v1/signals/generate", "method": "GET"},
    "risk_var": {"endpoint": "/api/v1/risk/var", "method": "GET"},
    "sentiment": {"endpoint": "/api/v1/analytics/sentiment", "method": "GET"},
    "ai_portfolio": {"endpoint": "/api/v1/ai/advisor/portfolio", "method": "POST"},
    "ai_market": {"endpoint": "/api/v1/ai/advisor/market", "method": "POST"},
    "ai_risk": {"endpoint": "/api/v1/ai/advisor/risk", "method": "POST"},
    "ai_query": {"endpoint": "/api/v1/ai/query", "method": "POST"},
    "fred": {"endpoint": "/api/v1/economics/fred", "method": "GET"},
}


@dataclass
class ParsedQuery:
    endpoint: str
    method: str
    params: dict
    confidence: float
    explanation: str = ""


_STOP_WORDS = frozenset({
    "the", "a", "an", "for", "of", "to", "in", "on", "at", "by", "with",
    "and", "or", "but", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "shall", "should", "may", "might", "show", "get", "me", "my",
    "price", "latest", "news", "all", "list", "top", "best", "worst",
    "what", "how", "who", "when", "where", "why", "this", "that",
    "whats", "its", "its", "im", "ive", "youre", "dont", "doesnt",
    "isnt", "arent", "wont", "cant", "couldnt", "wouldnt",
    "trading", "market",
})


def _extract_ticker(query: str) -> Optional[str]:
    words = re.findall(r'\b[A-Z]{1,10}\b', query, re.IGNORECASE)
    for word in words:
        upper = word.upper()
        if word.lower() not in _STOP_WORDS and len(upper) >= 2:
            return upper
    return None


def _regex_fallback(query: str) -> Optional[ParsedQuery]:
    q = query.lower()

    if re.search(r'\b(price|quote|trading at)\b', q):
        ticker = _extract_ticker(query)
        if ticker:
            return ParsedQuery(
                endpoint="/api/v1/market/live",
                method="GET",
                params={"tickers": ticker},
                confidence=0.8,
                explanation=f"Get live price for {ticker}",
            )

    if re.search(r'\b(portfolio|portfolios|my portfolio)\b', q):
        if re.search(r'\b(position|holding|own)\b', q):
            return ParsedQuery(
                endpoint="/api/v1/portfolios/{id}/positions",
                method="GET",
                params={},
                confidence=0.7,
                explanation="Get portfolio positions (requires portfolio ID)",
            )
        return ParsedQuery(
            endpoint="/api/v1/portfolios",
            method="GET",
            params={},
            confidence=0.8,
            explanation="List all portfolios",
        )

    if re.search(r'\b(news|headline)\b', q) or 'latest news' in q:
        ticker = _extract_ticker(query)
        if ticker:
            return ParsedQuery(
                endpoint="/api/v1/news/company/{ticker}",
                method="GET",
                params={"ticker": ticker},
                confidence=0.8,
                explanation=f"Get news for {ticker}",
            )
        return ParsedQuery(
            endpoint="/api/v1/news/market",
            method="GET",
            params={},
            confidence=0.7,
            explanation="Get market news",
        )

    if re.search(r'\b(fundamental|financial|income|earnings|balance sheet|cash flow)\b', q) or 'fundamentals' in q:
        ticker = _extract_ticker(query)
        if ticker:
            return ParsedQuery(
                endpoint="/api/v1/fundamentals/{ticker}",
                method="GET",
                params={"ticker": ticker},
                confidence=0.8,
                explanation=f"Get fundamentals for {ticker}",
            )

    if re.search(r'\b(option|chain|derivative)\b', q) or 'options' in q:
        ticker = _extract_ticker(query)
        if ticker:
            return ParsedQuery(
                endpoint="/api/v1/options/{ticker}",
                method="GET",
                params={"ticker": ticker},
                confidence=0.8,
                explanation=f"Get options chain for {ticker}",
            )

    if re.search(r'\b(mover|gainers|losers)\b', q) or 'movers' in q:
        return ParsedQuery(
            endpoint="/api/v1/market/movers",
            method="GET",
            params={},
            confidence=0.7,
            explanation="Get market movers",
        )

    if re.search(r'\b(sector|industry)\b', q) or 'sectors' in q:
        return ParsedQuery(
            endpoint="/api/v1/market/sectors",
            method="GET",
            params={},
            confidence=0.7,
            explanation="Get sector performance",
        )

    if re.search(r'\b(signal|trading signal)\b', q) or 'signals' in q:
        ticker = _extract_ticker(query)
        if ticker:
            return ParsedQuery(
                endpoint="/api/v1/signals/generate",
                method="GET",
                params={"ticker": ticker},
                confidence=0.7,
                explanation=f"Get trading signals for {ticker}",
            )

    if re.search(r'\b(watchlist|watch list)\b', q):
        return ParsedQuery(
            endpoint="/api/v1/watchlist/items",
            method="GET",
            params={},
            confidence=0.8,
            explanation="Get watchlist items",
        )

    if re.search(r'\b(fred|economic indicator|gdp|cpi|unemployment)\b', q):
        return ParsedQuery(
            endpoint="/api/v1/economics/fred",
            method="GET",
            params={},
            confidence=0.6,
            explanation="Get FRED economic data",
        )

    return None


async def parse_query(query: str) -> ParsedQuery:
    regex_result = _regex_fallback(query)
    if regex_result and regex_result.confidence >= 0.8:
        return regex_result

    try:
        client = AIClient(
            provider=settings.ai_provider or "openai",
            api_key=settings.ai_api_key,
            model=settings.ai_model,
        )
        prompt = PROMPT_TEMPLATE.format(query=sanitize_prompt(query))
        response = await client.chat([
            {"role": "system", "content": "You convert natural language to API calls. Return valid JSON only."},
            {"role": "user", "content": prompt},
        ])
        content = response.get("content", "")
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            cleaned = cleaned.rsplit("\n", 1)[0]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
        data = json.loads(cleaned)
        return ParsedQuery(
            endpoint=data.get("endpoint", ""),
            method=data.get("method", "GET"),
            params=data.get("params", {}),
            confidence=0.9,
            explanation=data.get("explanation", ""),
        )
    except Exception as e:
        logger.warning(f"AI NLQ parsing failed, using regex fallback: {e}")
        if regex_result:
            return regex_result
        return ParsedQuery(
            endpoint="",
            method="",
            params={},
            confidence=0.0,
            explanation="Could not parse query",
        )


async def execute_query(parsed: ParsedQuery) -> dict:
    if not parsed.endpoint:
        return {"error": "No endpoint could be determined from the query", "confidence": parsed.confidence}

    result = {
        "endpoint": parsed.endpoint,
        "method": parsed.method,
        "params": parsed.params,
        "confidence": parsed.confidence,
        "explanation": parsed.explanation,
    }

    if parsed.confidence < 0.5:
        result["warning"] = "Low confidence query — please verify the result"
        return result

    return result
