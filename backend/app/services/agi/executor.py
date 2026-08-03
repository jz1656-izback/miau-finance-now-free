"""Autonomous trade executor — execute AGI decisions with human-in-the-loop override."""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class TradeDecision:
    ticker: str
    side: str
    qty: float
    order_type: str = "market"
    confidence: float = 0.0
    reasoning: str = ""
    agent_id: str = ""


@dataclass
class ExecutionRecord:
    id: str
    decision: TradeDecision
    status: str
    executed_at: Optional[str] = None
    human_approved: bool = False
    error: Optional[str] = None


_executions: list[ExecutionRecord] = []
_human_in_the_loop: bool = True


async def set_human_in_the_loop(enabled: bool) -> None:
    global _human_in_the_loop
    _human_in_the_loop = enabled
    logger.info("Human-in-the-loop mode: %s", enabled)


async def execute_decision(decision: TradeDecision) -> dict[str, Any]:
    import uuid
    record = ExecutionRecord(
        id=str(uuid.uuid4())[:8],
        decision=decision,
        status="pending_approval" if _human_in_the_loop else "approved",
        human_approved=not _human_in_the_loop,
    )

    if _human_in_the_loop:
        logger.info("Trade %s pending human approval: %s %s %.2f", record.id, decision.side, decision.ticker, decision.qty)
        _executions.append(record)
        return {
            "execution_id": record.id,
            "status": "pending_approval",
            "message": f"Approval needed: {decision.side} {decision.qty} {decision.ticker}",
            "decision": {"ticker": decision.ticker, "side": decision.side, "qty": decision.qty, "confidence": decision.confidence, "reasoning": decision.reasoning},
        }

    return await _submit(record)


async def approve_execution(execution_id: str) -> dict[str, Any]:
    for record in _executions:
        if record.id == execution_id and record.status == "pending_approval":
            record.human_approved = True
            return await _submit(record)
    return {"error": "Execution not found or already processed", "execution_id": execution_id}


async def reject_execution(execution_id: str) -> dict[str, Any]:
    for record in _executions:
        if record.id == execution_id and record.status == "pending_approval":
            record.status = "rejected"
            logger.info("Trade %s rejected by human", execution_id)
            return {"execution_id": execution_id, "status": "rejected"}
    return {"error": "Execution not found"}


async def list_pending() -> list[dict[str, Any]]:
    return [
        {
            "execution_id": r.id,
            "ticker": r.decision.ticker,
            "side": r.decision.side,
            "qty": r.decision.qty,
            "confidence": r.decision.confidence,
            "reasoning": r.decision.reasoning,
            "agent_id": r.decision.agent_id,
            "status": r.status,
        }
        for r in _executions if r.status == "pending_approval"
    ]


async def list_history(limit: int = 20) -> list[dict[str, Any]]:
    return [
        {
            "execution_id": r.id,
            "ticker": r.decision.ticker,
            "side": r.decision.side,
            "qty": r.decision.qty,
            "status": r.status,
            "human_approved": r.human_approved,
            "executed_at": r.executed_at,
            "error": r.error,
        }
        for r in _executions[-limit:]
    ]


async def _submit(record: ExecutionRecord) -> dict[str, Any]:
    import uuid
    import random
    record.status = "submitted"
    record.executed_at = datetime.now(timezone.utc).isoformat()
    _executions.append(record)

    order_id = str(uuid.uuid4())[:12]
    logger.info("Trade %s submitted: %s %s %.2f (order %s)", record.id, record.decision.side, record.decision.ticker, record.decision.qty, order_id)
    return {
        "execution_id": record.id,
        "order_id": order_id,
        "status": "submitted",
        "ticker": record.decision.ticker,
        "side": record.decision.side,
        "qty": record.decision.qty,
        "executed_at": record.executed_at,
        "simulated_fill_price": round(random.uniform(95, 105), 2),
    }
