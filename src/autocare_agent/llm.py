import json
from typing import Protocol
from uuid import UUID

import httpx
from pydantic import ValidationError

from autocare_agent.schemas import ConversationContext, Intent, LLMResult

SYSTEM_PROMPT = """You are an administrative conversation assistant.
Never diagnose, invent prices, discounts, availability, or confirmations.
Critical actions must be proposed as structured actions for the internal application.
Return only a JSON object matching the requested contract."""


class LLMError(Exception):
    """Base error for controlled provider failures."""


class DependencyUnavailable(LLMError):
    """The provider could not be reached or timed out."""


class InvalidDependencyResponse(LLMError):
    """The provider returned content outside the expected contract."""


class LLMProvider(Protocol):
    async def generate(self, system_prompt: str, message: str, request_id: UUID) -> LLMResult: ...


def build_system_prompt(context: ConversationContext | None, intent: Intent) -> str:
    safe_parts = [SYSTEM_PROMPT, f"intent={intent.value}"]
    if context:
        if context.locale:
            safe_parts.append(f"locale={context.locale}")
        if context.timezone:
            safe_parts.append(f"timezone={context.timezone}")
        if context.resumo_sessao:
            safe_parts.append(f"session_summary={context.resumo_sessao[:500]}")
    return "\n".join(safe_parts)


class ComposerLLMProvider:
    def __init__(self, client: httpx.AsyncClient, base_url: str, api_key: str, model: str, timeout: float) -> None:
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    async def generate(self, system_prompt: str, message: str, request_id: UUID) -> LLMResult:
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": message}],
            "response_format": {"type": "json_object"},
        }
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "X-Request-ID": str(request_id)},
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise DependencyUnavailable("llm_unavailable") from exc

        try:
            raw = response.json()["choices"][0]["message"]["content"]
            return LLMResult.model_validate(json.loads(raw))
        except (KeyError, TypeError, json.JSONDecodeError, ValidationError) as exc:
            raise InvalidDependencyResponse("invalid_llm_response") from exc
