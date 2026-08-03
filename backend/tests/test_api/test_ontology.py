import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_get_ontology_types(client: AsyncClient):
    resp = await client.get("/api/v1/ontology/types")
    assert resp.status_code in [200, 401]
