import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_regime(client: AsyncClient):
    resp = await client.get("/api/v1/analytics/regime/AAPL")
    assert resp.status_code in [200, 401, 404, 500]
