import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_search(client: AsyncClient):
    resp = await client.get("/api/v1/search?q=test")
    assert resp.status_code in [200, 401]
