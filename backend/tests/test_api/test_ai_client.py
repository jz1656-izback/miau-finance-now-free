import pytest
from unittest.mock import AsyncMock, MagicMock
from httpx import HTTPStatusError, Request, Response

from app.services.ai.client import AIClient, AIClientError


@pytest.fixture
def client():
    return AIClient(provider="openai", api_key="test-key", model="gpt-4o-mini")


@pytest.mark.anyio
async def test_init_openai():
    c = AIClient(provider="openai", api_key="sk-test", model="gpt-4o-mini")
    assert c.provider == "openai"
    assert c.model == "gpt-4o-mini"


@pytest.mark.anyio
async def test_init_anthropic():
    c = AIClient(provider="anthropic", api_key="sk-ant-test", model="claude-3-haiku-20240307")
    assert c.provider == "anthropic"


@pytest.mark.anyio
async def test_init_invalid_provider():
    with pytest.raises(AIClientError, match="Unsupported provider"):
        AIClient(provider="invalid", api_key="test", model="test")


@pytest.mark.anyio
async def test_chat_success(client):
    client._client = AsyncMock()
    client._client.post.return_value = MagicMock(
        status_code=200,
        json=lambda: {"choices": [{"message": {"content": "Hello!"}}]},
    )
    result = await client.chat([{"role": "user", "content": "hi"}])
    assert result["content"] == "Hello!"
    assert result["role"] == "assistant"


@pytest.mark.anyio
async def test_chat_rate_limit_retry(client):
    call_count = 0

    def mock_post(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        resp = MagicMock()
        if call_count < 3:
            resp.status_code = 429
        else:
            resp.status_code = 200
            resp.json.return_value = {"choices": [{"message": {"content": "OK"}}]}
        return resp

    client._client = AsyncMock()
    client._client.post.side_effect = mock_post
    result = await client.chat([{"role": "user", "content": "hi"}])
    assert result["content"] == "OK"
    assert call_count == 3


@pytest.mark.anyio
async def test_chat_http_error(client):
    client._client = AsyncMock()
    req = Request("POST", "https://example.com")
    resp = Response(500, request=req)
    client._client.post.side_effect = HTTPStatusError("Server error", request=req, response=resp)

    with pytest.raises(AIClientError, match="AI provider error"):
        await client.chat([{"role": "user", "content": "hi"}])


@pytest.mark.anyio
async def test_chat_timeout_retry(client):
    import httpx
    call_count = 0

    def mock_post(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise httpx.TimeoutException("timeout")
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"choices": [{"message": {"content": "OK"}}]}
        return resp

    client._client = AsyncMock()
    client._client.post.side_effect = mock_post
    result = await client.chat([{"role": "user", "content": "hi"}])
    assert result["content"] == "OK"
    assert call_count == 3


@pytest.mark.anyio
async def test_chat_all_retries_fail(client):
    client._client = AsyncMock()
    client._client.post.return_value = MagicMock(status_code=429)

    with pytest.raises(AIClientError, match="Failed to get AI response"):
        await client.chat([{"role": "user", "content": "hi"}])


@pytest.mark.anyio
async def test_chat_stream(client):
    mock_chunks = iter([
        b"data: {\"choices\": [{\"delta\": {\"content\": \"Hello\"}}]}\n\n",
        b"data: {\"choices\": [{\"delta\": {\"content\": \" World\"}}]}\n\n",
        b"data: [DONE]\n\n",
    ])

    async def aiter_lines():
        for chunk in mock_chunks:
            yield chunk.decode()

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.aiter_lines = aiter_lines

    mock_stream = MagicMock()
    mock_stream.__aenter__.return_value = mock_resp
    mock_stream.__aexit__.return_value = None

    mock_client = MagicMock()
    mock_client.stream.return_value = mock_stream

    client._client = mock_client

    chunks = []
    async for chunk in client.chat_stream([{"role": "user", "content": "hi"}]):
        chunks.append(chunk)
    assert "".join(chunks) == "Hello World"


@pytest.mark.anyio
async def test_chat_stream_rate_limited(client):
    mock_resp = MagicMock()
    mock_resp.status_code = 429

    mock_stream = MagicMock()
    mock_stream.__aenter__.return_value = mock_resp
    mock_stream.__aexit__.return_value = None

    mock_client = MagicMock()
    mock_client.stream.return_value = mock_stream

    client._client = mock_client

    chunks = []
    async for chunk in client.chat_stream([{"role": "user", "content": "hi"}]):
        chunks.append(chunk)
    assert any("rate limit" in c.lower() for c in chunks)


@pytest.mark.anyio
async def test_close(client):
    client._client = AsyncMock()
    await client.close()
    assert client._client is None
