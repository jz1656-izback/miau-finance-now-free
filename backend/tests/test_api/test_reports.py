import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_reports(client: AsyncClient):
    resp = await client.get("/api/v1/reports/trades/csv")
    assert resp.status_code in [200, 401]
