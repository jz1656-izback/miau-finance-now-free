import asyncio
import json
import logging
import random
from typing import Any, AsyncGenerator, Optional

import httpx

logger = logging.getLogger(__name__)

OPENAI_BASE_URL = "https://api.openai.com/v1"
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1"


class AIClientError(Exception):
    pass


class AIClient:
    def __init__(self, provider: str, api_key: str, model: str) -> None:
        self.provider = provider.lower()
        self.api_key = api_key
        self.model = model
        self._client: Optional[httpx.AsyncClient] = None

        if self.provider not in ("openai", "anthropic"):
            raise AIClientError(f"Unsupported provider: {provider}")

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=60.0)
        return self._client

    def _build_headers(self) -> dict[str, str]:
        if self.provider == "openai":
            return {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        return {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

    def _chat_url(self) -> str:
        return f"{OPENAI_BASE_URL}/chat/completions" if self.provider == "openai" else f"{ANTHROPIC_BASE_URL}/messages"

    def _build_payload(self, messages: list[dict[str, str]], stream: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7,
        }
        if stream:
            payload["stream"] = True
        return payload

    async def chat(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        client = await self._get_client()
        url = self._chat_url()
        headers = self._build_headers()
        payload = self._build_payload(messages, stream=False)

        for attempt in range(3):
            try:
                response = await client.post(url, json=payload, headers=headers)
                if response.status_code == 429:
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning("Rate limited, retrying in %.2fs (attempt %d)", delay, attempt + 1)
                    await asyncio.sleep(delay)
                    continue
                response.raise_for_status()
                data = response.json()
                return self._parse_response(data)
            except httpx.TimeoutException:
                logger.warning("Timeout on attempt %d", attempt + 1)
                if attempt == 2:
                    raise AIClientError("AI provider timeout after 3 retries")
                await asyncio.sleep(1)
            except httpx.HTTPStatusError as e:
                logger.error("HTTP status error: %s", e)
                raise AIClientError(f"AI provider error: {e}")
            except httpx.HTTPError as e:
                logger.error("HTTP error: %s", e)
                raise AIClientError(f"AI provider error: {e}")

        raise AIClientError("Failed to get AI response after 3 retries")

    async def chat_stream(self, messages: list[dict[str, str]]) -> AsyncGenerator[str, None]:
        client = await self._get_client()
        url = self._chat_url()
        headers = self._build_headers()
        payload = self._build_payload(messages, stream=True)

        async with client.stream("POST", url, json=payload, headers=headers) as response:
            if response.status_code == 429:
                logger.warning("Rate limited during stream request")
                yield json.dumps({"error": "Rate limited. Please try again."})
                return
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    chunk = line[6:]
                    if chunk.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(chunk)
                        content = self._extract_stream_content(data)
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue

    def _parse_response(self, data: dict[str, Any]) -> dict[str, Any]:
        if self.provider == "openai":
            try:
                content = data["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                content = str(data)
            return {"content": content, "role": "assistant", "provider": "openai"}
        try:
            content = data["content"][0]["text"]
        except (KeyError, IndexError):
            content = str(data)
        return {"content": content, "role": "assistant", "provider": "anthropic"}

    def _extract_stream_content(self, chunk: dict[str, Any]) -> Optional[str]:
        if self.provider == "openai":
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            return delta.get("content")
        delta = chunk.get("delta", {})
        return delta.get("text")

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
