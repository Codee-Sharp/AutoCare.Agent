import json
from uuid import UUID

import httpx
from pydantic import ValidationError

from autocare_agent.domain.errors import DependencyUnavailable, InvalidDependencyResponse
from autocare_agent.domain.models import Intent, LLMResult


class FakeLLMProvider:
    async def generate(self, system_prompt: str, message: str, request_id: UUID) -> LLMResult:
        lowered = message.lower()
        intent = Intent.GENERAL
        if "horário" in lowered or "disponibilidade" in lowered:
            intent = Intent.AVAILABILITY
        elif "serviço" in lowered:
            intent = Intent.SERVICE
        elif "desconto" in lowered:
            intent = Intent.DISCOUNT
        return LLMResult(resposta_texto="Posso ajudar com essa solicitação administrativa.", intencao=intent)


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
            raw = response.json()["choices"][0]["message"]["content"]
            return LLMResult.model_validate(json.loads(raw))
        except (httpx.HTTPError, KeyError, TypeError, json.JSONDecodeError, ValidationError) as exc:
            if isinstance(exc, httpx.TimeoutException):
                raise DependencyUnavailable("llm_timeout") from exc
            raise InvalidDependencyResponse("invalid_llm_response") from exc
