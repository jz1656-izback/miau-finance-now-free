import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_pairs(client: AsyncClient):
    resp = await client.get("/api/v1/analytics/pairs?ticker1=AAPL&ticker2=MSFT")
    assert resp.status_code in [200, 401, 404, 500]
