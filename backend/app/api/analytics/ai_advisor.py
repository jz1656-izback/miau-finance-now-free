from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db
from app.services.ai.advisor import analyze_portfolio, analyze_market, assess_risk
from app.services.ai.workflow import (
    create_workflow, get_workflow, list_workflows, delete_workflow,
    run_workflow_once, parse_workflow_description,
)

router = APIRouter()


class PortfolioRequest(BaseModel):
    portfolio_id: str


class RiskRequest(BaseModel):
    portfolio_id: str


class QueryRequest(BaseModel):
    query: str


class WorkflowCreateRequest(BaseModel):
    name: str
    description: str
    ticker: str
    conditions: list[dict]
    steps: list[dict]
    run_interval_seconds: Optional[int] = None


class WorkflowParseRequest(BaseModel):
    text: str


@router.post("/advisor/portfolio")
async def advisor_portfolio(
    req: PortfolioRequest,
    user=Depends(get_current_user),
):
    try:
        return await analyze_portfolio(req.portfolio_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advisor/market")
async def advisor_market(
    user=Depends(get_current_user),
):
    try:
        return await analyze_market()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advisor/risk")
async def advisor_risk(
    req: RiskRequest,
    user=Depends(get_current_user),
):
    try:
        return await assess_risk(req.portfolio_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def ai_query(
    req: QueryRequest,
    user=Depends(get_current_user),
):
    from app.services.ai.client import AIClient
    from app.services.ai.advisor import sanitize_prompt
    from app.config import settings

    if not settings.ai_api_key:
        raise HTTPException(status_code=503, detail="AI not configured")
    client = AIClient(
        provider=settings.ai_provider or "openai",
        api_key=settings.ai_api_key,
        model=settings.ai_model or "gpt-4o-mini",
    )
    try:
        result = await client.chat([
            {"role": "system", "content": "You are a financial assistant. Answer concisely."},
            {"role": "user", "content": sanitize_prompt(req.query)},
        ])
        return {"response": result.get("content", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/workflows/parse")
async def parse_workflow(req: WorkflowParseRequest):
    result = parse_workflow_description(req.text)
    if not result or (not result["conditions"] and not result["steps"]):
        raise HTTPException(400, "Could not parse workflow from text. Try: 'buy AAPL if RSI < 30 and price < 200'")
    return result


@router.post("/workflows")
async def api_create_workflow(
    req: WorkflowCreateRequest,
    user=Depends(get_current_user_db),
):
    wf = await create_workflow(
        name=req.name,
        description=req.description,
        ticker=req.ticker,
        conditions=req.conditions,
        steps=req.steps,
        run_interval_seconds=req.run_interval_seconds,
    )
    return wf.to_dict()


@router.get("/workflows")
async def api_list_workflows():
    return [wf.to_dict() for wf in list_workflows()]


@router.get("/workflows/{workflow_id}")
async def api_get_workflow(workflow_id: str):
    wf = get_workflow(workflow_id)
    if not wf:
        raise HTTPException(404, "Workflow not found")
    return wf.to_dict()


@router.delete("/workflows/{workflow_id}")
async def api_delete_workflow(workflow_id: str):
    if not delete_workflow(workflow_id):
        raise HTTPException(404, "Workflow not found")
    return {"deleted": workflow_id}


@router.post("/workflows/{workflow_id}/run")
async def api_run_workflow(workflow_id: str):
    result = await run_workflow_once(workflow_id)
    if "error" in result:
        raise HTTPException(404, result["error"])
    return result
