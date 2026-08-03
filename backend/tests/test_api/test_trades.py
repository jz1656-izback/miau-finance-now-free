import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_get_trades(client: AsyncClient):
    resp = await client.get("/api/v1/trades")
    assert resp.status_code in [200, 401]
