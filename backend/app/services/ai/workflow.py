import asyncio
import json
import logging
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Optional

from app.async_utils import safe_task

import httpx

from app.config import settings
from app.services.ai.client import AIClient
from app.services.ai.advisor import sanitize_prompt

logger = logging.getLogger(__name__)

CONDITION_PATTERNS = [
    (re.compile(r"rsi\s*(<|<=|>|>=|=)\s*(\d+)", re.I), "rsi"),
    (re.compile(r"price\s*(<|<=|>|>=|=)\s*([\d.]+)", re.I), "price"),
    (re.compile(r"volume\s*(<|<=|>|>=|=)\s*([\d.]+)", re.I), "volume"),
    (re.compile(r"change%\s*(<|<=|>|>=|=)\s*([\d.-]+)", re.I), "change_pct"),
    (re.compile(r"(sma|ma)\s*(<|<=|>|>=|=)\s*([\d.]+)", re.I), "sma"),
    (re.compile(r"(macd)\s*(cross|above|below)", re.I), "macd"),
    (re.compile(r"(trend|direction)\s*(is|==)\s*(bullish|bearish)", re.I), "trend"),
]

ACTION_PATTERNS = [
    (re.compile(r"buy\s+(\w+)", re.I), "buy"),
    (re.compile(r"sell\s+(\w+)", re.I), "sell"),
    (re.compile(r"alert\s+(?:on|for)?\s*(\w+)", re.I), "alert"),
    (re.compile(r"notify\s+(?:on|about)?\s*(\w+)", re.I), "notify"),
]


@dataclass
class Condition:
    field: str
    operator: str
    value: float

    def evaluate(self, current_value: float) -> bool:
        if self.operator == "<":
            return current_value < self.value
        elif self.operator == "<=":
            return current_value <= self.value
        elif self.operator == ">":
            return current_value > self.value
        elif self.operator == ">=":
            return current_value >= self.value
        elif self.operator == "=" or self.operator == "==":
            return abs(current_value - self.value) < 0.001
        return False

    def to_dict(self) -> dict:
        return {"field": self.field, "operator": self.operator, "value": self.value}


@dataclass
class WorkflowStep:
    action: str
    ticker: str
    quantity: Optional[int] = None
    order_type: str = "market"
    params: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "action": self.action,
            "ticker": self.ticker,
            "quantity": self.quantity,
            "order_type": self.order_type,
            "params": self.params,
        }


@dataclass
class Workflow:
    id: str
    name: str
    description: str
    ticker: str
    conditions: list[Condition]
    steps: list[WorkflowStep]
    is_active: bool = True
    run_interval_seconds: Optional[int] = None
    last_run_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    run_count: int = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ticker": self.ticker,
            "conditions": [c.to_dict() for c in self.conditions],
            "steps": [s.to_dict() for s in self.steps],
            "is_active": self.is_active,
            "run_interval_seconds": self.run_interval_seconds,
            "last_run_at": self.last_run_at.isoformat() if self.last_run_at else None,
            "created_at": self.created_at.isoformat(),
            "run_count": self.run_count,
        }


_workflows: dict[str, Workflow] = {}
_tasks: dict[str, asyncio.Task] = {}


def _generate_id() -> str:
    import uuid
    return str(uuid.uuid4())[:8]


async def _fetch_ticker_data(ticker: str) -> dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            base_url = settings.cubejs_api_url or "http://localhost:4000"
            resp = await client.get(
                f"{base_url}/api/v1/market/live?tickers={ticker}",
            )
            if resp.status_code == 200:
                return resp.json().get("data", {}).get(ticker, {})
    except Exception as e:
        logger.warning("Failed to fetch live data for %s: %s", ticker, e)

    try:
        from app.services.analytics.market_data import get_market_data
        data = await get_market_data(ticker)
        if data:
            return data
    except Exception as e:
        logger.warning("Failed to fetch market data for %s: %s", ticker, e)

    return {}


async def _fetch_rsi(ticker: str) -> Optional[float]:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            base_url = settings.cubejs_api_url or "http://localhost:4000"
            resp = await client.get(
                f"{base_url}/api/v1/signals/generate?ticker={ticker}&period=3mo",
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("indicators", {}).get("rsi_14")
    except Exception as e:
        logger.warning("Failed to fetch RSI for %s: %s", ticker, e)
    return None


def parse_workflow_description(text: str) -> Optional[dict]:
    text = text.strip()
    result: dict[str, Any] = {"conditions": [], "steps": [], "ticker": None, "name": None}

    for pattern, name in CONDITION_PATTERNS:
        for match in pattern.finditer(text):
            if name in ("rsi", "price", "volume", "change_pct", "sma"):
                result["conditions"].append({
                    "field": name,
                    "operator": match.group(1),
                    "value": float(match.group(2)),
                })
            elif name == "macd":
                result["conditions"].append({
                    "field": "macd",
                    "operator": match.group(2),
                    "value": 0,
                })
            elif name == "trend":
                result["conditions"].append({
                    "field": "trend",
                    "operator": "==",
                    "value": match.group(3),
                })

    for pattern, name in ACTION_PATTERNS:
        for match in pattern.finditer(text):
            ticker = match.group(1).upper()
            result["steps"].append({"action": name, "ticker": ticker})
            if not result["ticker"]:
                result["ticker"] = ticker

    tickers_in_text = re.findall(r"\b[A-Z]{1,5}\b", text.upper())
    valid_tickers = [t for t in tickers_in_text if t not in {"RSI", "SMA", "MACD", "BUY", "SELL"}]
    if not result["ticker"] and valid_tickers:
        result["ticker"] = valid_tickers[0]

    result["name"] = text[:60].rstrip(".!")
    return result


async def evaluate_conditions(conditions: list[Condition], ticker: str) -> tuple[bool, dict[str, Any]]:
    data = await _fetch_ticker_data(ticker)
    rsi = await _fetch_rsi(ticker)

    values: dict[str, float] = {
        "price": float(data.get("price", data.get("close", 0))),
        "volume": float(data.get("volume", 0)),
        "change_pct": float(data.get("change_pct", data.get("change", 0))),
        "rsi": rsi or 50.0,
        "trend": 1.0 if data.get("trend", "neutral") in ("bullish", "up") else 0.0,
    }

    all_met = True
    results = []
    for c in conditions:
        current = values.get(c.field, 0)
        met = c.evaluate(current)
        results.append({"field": c.field, "operator": c.operator, "threshold": c.value, "current": current, "met": met})
        if not met:
            all_met = False

    return all_met, {"ticker": ticker, "values": values, "results": results, "all_conditions_met": all_met}


async def execute_steps(steps: list[WorkflowStep], user_id: str, db_session=None) -> list[dict]:
    results = []
    headers = {"Authorization": f"Bearer {settings.secret_key}"}
    base_url = f"http://localhost:{settings.port if hasattr(settings, 'port') else 8000}"

    for step in steps:
        try:
            if step.action == "buy":
                qty = step.quantity or 1
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.post(
                        f"{base_url}/api/v1/orders",
                        json={
                            "ticker": step.ticker,
                            "side": "BUY",
                            "quantity": qty,
                            "order_type": step.order_type,
                            "portfolio_id": step.params.get("portfolio_id"),
                        },
                        headers=headers,
                    )
                    results.append({"action": "buy", "ticker": step.ticker, "status": resp.status_code, "response": await resp.json()})

            elif step.action == "sell":
                qty = step.quantity or 1
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.post(
                        f"{base_url}/api/v1/orders",
                        json={
                            "ticker": step.ticker,
                            "side": "SELL",
                            "quantity": qty,
                            "order_type": step.order_type,
                            "portfolio_id": step.params.get("portfolio_id"),
                        },
                        headers=headers,
                    )
                    results.append({"action": "sell", "ticker": step.ticker, "status": resp.status_code, "response": await resp.json()})

            elif step.action == "alert":
                results.append({"action": "alert", "ticker": step.ticker, "status": "triggered"})

            elif step.action == "notify":
                results.append({"action": "notify", "ticker": step.ticker, "status": "sent"})

        except Exception as e:
            logger.error("Workflow step failed: %s", e)
            results.append({"action": step.action, "ticker": step.ticker, "status": "error", "error": str(e)})

    return results


async def create_workflow(
    name: str,
    description: str,
    ticker: str,
    conditions: list[dict],
    steps: list[dict],
    run_interval_seconds: Optional[int] = None,
) -> Workflow:
    wf = Workflow(
        id=_generate_id(),
        name=name,
        description=description,
        ticker=ticker.upper(),
        conditions=[Condition(**c) for c in conditions],
        steps=[WorkflowStep(**s) for s in steps],
        run_interval_seconds=run_interval_seconds,
    )
    _workflows[wf.id] = wf
    logger.info("Workflow created: %s (%s)", wf.name, wf.id)

    if run_interval_seconds and run_interval_seconds > 0:
        _start_scheduled_workflow(wf.id)

    return wf


def get_workflow(workflow_id: str) -> Optional[Workflow]:
    return _workflows.get(workflow_id)


def list_workflows() -> list[Workflow]:
    return list(_workflows.values())


def delete_workflow(workflow_id: str) -> bool:
    if workflow_id in _tasks:
        _tasks[workflow_id].cancel()
        del _tasks[workflow_id]
    return _workflows.pop(workflow_id, None) is not None


def _start_scheduled_workflow(workflow_id: str):
    async def _run_loop():
        wf = _workflows.get(workflow_id)
        if not wf:
            return
        while wf.is_active:
            await asyncio.sleep(wf.run_interval_seconds or 3600)
            if not wf.is_active:
                break
            try:
                all_met, eval_result = await evaluate_conditions(wf.conditions, wf.ticker)
                if all_met:
                    results = await execute_steps(wf.steps, "system")
                    logger.info("Workflow %s triggered: %s", wf.name, results)
                wf.run_count += 1
                wf.last_run_at = datetime.now(timezone.utc)
            except Exception as e:
                logger.error("Workflow %s run error: %s", wf.name, e)

    _tasks[workflow_id] = safe_task(
        _run_loop(), name=f"workflow-{workflow_id[:8]}"
    )


async def run_workflow_once(workflow_id: str) -> dict:
    wf = _workflows.get(workflow_id)
    if not wf:
        return {"error": "Workflow not found"}

    all_met, eval_result = await evaluate_conditions(wf.conditions, wf.ticker)
    wf.run_count += 1
    wf.last_run_at = datetime.now(timezone.utc)

    if not all_met:
        return {"evaluation": eval_result, "executed": False, "reason": "Conditions not met"}

    results = await execute_steps(wf.steps, "system")
    return {"evaluation": eval_result, "executed": True, "results": results}
