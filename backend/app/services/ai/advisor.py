import json
import logging
import re
from datetime import timezone, datetime
from typing import Any, Optional

from app.services.notification_service import send_web_push, notification_history

from app.cache import get_cache, set_cache
from app.config import settings
from app.services.ai.client import AIClient
from app.services.ai.context import build_market_context, build_risk_context, truncate_context
from app.services.ai.prompts.market import PROMPT_TEMPLATE as MARKET_PROMPT
from app.services.ai.prompts.risk import PROMPT_TEMPLATE as RISK_PROMPT

logger = logging.getLogger(__name__)

CACHE_TTL = 3600

_PORTFOLIO_PROMPT = """You are a financial analyst. Analyze this portfolio and give actionable recommendations.

Portfolio context:
{holdings}
{performance}
{risk_metrics}

Provide your analysis in the following JSON format:
{{
    "summary": "brief overview of portfolio health",
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "risk_level": "low|medium|high"
}}
"""


def _get_client() -> Optional[AIClient]:
    if not settings.ai_api_key:
        logger.warning("AI_API_KEY not configured")
        return None
    return AIClient(
        provider=settings.ai_provider or "openai",
        api_key=settings.ai_api_key,
        model=settings.ai_model or "gpt-4o-mini",
    )


def sanitize_input(text: str) -> str:
    original = text

    text = re.sub(r"(?i)(system|assistant|human):", "", text)
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"(?i)(ignore|forget|override|disregard)\s+(all\s+)?(previous|above|instructions|prompts)", "", text)
    text = re.sub(r"(?i)<!--.*?-->", "", text)
    text = re.sub(r"(?i)```.*?```", "", text, flags=re.DOTALL)
    text = text[:1000]
    text = text.strip()

    if text != original:
        logger.warning("Prompt sanitization triggered on input (length %d -> %d)", len(original), len(text))

    return text


def sanitize_prompt(prompt: str) -> str:
    """Sanitize user prompt before sending to AI.

    Removes prompt injection patterns, system prompt override attempts,
    HTML/script tags, markdown code blocks, and limits input length to 1000 characters.

    Args:
        prompt: Raw user input.

    Returns:
        Sanitized prompt string.
    """
    return sanitize_input(prompt)


async def analyze_portfolio(portfolio_id: str, context: Optional[dict] = None) -> dict[str, Any]:
    cache_key = f"ai:portfolio:{portfolio_id}"
    cached = await get_cache(cache_key)
    if cached:
        return cached

    client = _get_client()
    if not client:
        return {"error": "AI not configured"}

    if context is None:
        context = {"holdings": "N/A", "performance": "N/A", "risk_metrics": "N/A"}

    context, _ = truncate_context(context)
    prompt = _PORTFOLIO_PROMPT.format(**context)

    try:
        result = await client.chat([
            {"role": "system", "content": "You are a financial analyst. Respond in JSON."},
            {"role": "user", "content": prompt},
        ])
        content = result.get("content", "")
        parsed = _parse_json_response(content)
        await set_cache(cache_key, parsed, ex=CACHE_TTL)
        return parsed
    except Exception as e:
        logger.error("Portfolio analysis failed: %s", e)
        return {"error": str(e)}
    finally:
        await client.close()


async def analyze_market() -> dict[str, Any]:
    cache_key = "ai:market:overview"
    cached = await get_cache(cache_key)
    if cached:
        return cached

    client = _get_client()
    if not client:
        return {"error": "AI not configured"}

    ctx = await build_market_context()
    ctx, _ = truncate_context(ctx)
    prompt = MARKET_PROMPT.format(**ctx)

    try:
        result = await client.chat([
            {"role": "system", "content": "You are a market analyst. Respond in JSON."},
            {"role": "user", "content": prompt},
        ])
        content = result.get("content", "")
        parsed = _parse_json_response(content)
        await set_cache(cache_key, parsed, ex=CACHE_TTL)
        return parsed
    except Exception as e:
        logger.error("Market analysis failed: %s", e)
        return {"error": str(e)}
    finally:
        await client.close()


async def assess_risk(portfolio_id: str) -> dict[str, Any]:
    cache_key = f"ai:risk:{portfolio_id}"
    cached = await get_cache(cache_key)
    if cached:
        return cached

    client = _get_client()
    if not client:
        return {"error": "AI not configured"}

    ctx = await build_risk_context(portfolio_id)
    ctx, _ = truncate_context(ctx)
    prompt = RISK_PROMPT.format(**ctx)

    try:
        result = await client.chat([
            {"role": "system", "content": "You are a risk analyst. Respond in JSON."},
            {"role": "user", "content": prompt},
        ])
        content = result.get("content", "")
        parsed = _parse_json_response(content)
        await set_cache(cache_key, parsed, ex=CACHE_TTL)
        return parsed
    except Exception as e:
        logger.error("Risk assessment failed: %s", e)
        return {"error": str(e)}
    finally:
        await client.close()


async def notify_ai_ready(user_id: str, analysis_type: str, ticker: Optional[str] = None, portfolio_id: Optional[str] = None) -> bool:
    """Send push notification when AI analysis completes.

    Args:
        user_id: User to notify.
        analysis_type: 'portfolio', 'market', 'risk', or 'query'.
        ticker: Optional ticker for market/query analyses.
        portfolio_id: Optional portfolio ID for portfolio/risk analyses.
    """
    if analysis_type == "portfolio" and portfolio_id:
        title = "🤖 AI Portfolio Analysis Ready"
        body = f"Your portfolio analysis is complete. Check the insights!"
        deep_link = f"ai portfolio {portfolio_id}"
    elif analysis_type == "market":
        title = "🤖 AI Market Analysis Ready"
        body = f"Market overview analysis is ready. See what's moving!"
        deep_link = "ai market"
    elif analysis_type == "risk" and portfolio_id:
        title = "🤖 AI Risk Assessment Ready"
        body = f"Risk assessment for your portfolio is complete."
        deep_link = f"ai risk {portfolio_id}"
    elif analysis_type == "query" and ticker:
        title = "🤖 AI Query Complete"
        body = f"AI analysis for {ticker} is ready."
        deep_link = f"ai query {ticker}"
    else:
        return False

    success = await send_web_push(user_id, title, body)
    notification_history.record({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "channel": "push",
        "type": "ai_ready",
        "status": "sent" if success else "failed",
        "data": {"analysis_type": analysis_type, "ticker": ticker, "portfolio_id": portfolio_id, "deep_link": deep_link},
    })
    logger.info(f"AI ready notification for {user_id}: {title}")
    return success


def _parse_json_response(content: str) -> dict[str, Any]:
    content = content.strip()
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
    return {"raw_response": content}
