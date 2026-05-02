import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_returns_ok(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_response_body(client: AsyncClient):
    response = await client.get("/health")
    body = response.json()
    assert body["status"] == "ok"
    assert body["environment"] == "local"
