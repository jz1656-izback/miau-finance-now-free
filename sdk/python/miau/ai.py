"""AI Advisor module for the Miau Finance Python SDK."""

from typing import Any, Optional

from miau import MiauClient


class AIModule:
    """Access AI advisor and natural language query endpoints."""

    def __init__(self, client: MiauClient):
        self._client = client

    def query(self, text: str) -> dict:
        return self._client.post("/api/v1/ai/query", {"query": text})

    def advisor_portfolio(self, portfolio_id: str) -> dict:
        return self._client.post("/api/v1/ai/advisor/portfolio", {"portfolio_id": portfolio_id})

    def advisor_market(self) -> dict:
        return self._client.post("/api/v1/ai/advisor/market")

    def advisor_risk(self, portfolio_id: str) -> dict:
        return self._client.post("/api/v1/ai/advisor/risk", {"portfolio_id": portfolio_id})

    def list_workflows(self) -> list[dict]:
        return self._client.get("/api/v1/ai/workflows")

    def create_workflow(self, name: str, ticker: str, conditions: list[dict], steps: list[dict],
                        run_interval_seconds: Optional[int] = None) -> dict:
        return self._client.post("/api/v1/ai/workflows", {
            "name": name, "ticker": ticker, "conditions": conditions,
            "steps": steps, "run_interval_seconds": run_interval_seconds,
        })

    def run_workflow(self, workflow_id: str) -> dict:
        return self._client.post(f"/api/v1/ai/workflows/{workflow_id}/run")
