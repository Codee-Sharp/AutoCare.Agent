from uuid import uuid4

import httpx
import pytest
import respx

from autocare_agent.llm import (
    ComposerAuthenticationFailed,
    ComposerLLMProvider,
    ComposerRequestRejected,
    DependencyUnavailable,
    InvalidDependencyResponse,
    build_system_prompt,
)
from autocare_agent.schemas import ConversationContext, Intent


@pytest.mark.asyncio
@respx.mock
async def test_composer_rejects_invalid_content() -> None:
    respx.post("https://composer.test/chat/completions").mock(
        return_value=httpx.Response(200, json={"choices": [{"message": {"content": "invalid"}}]})
    )
    provider = ComposerLLMProvider(httpx.AsyncClient(), "https://composer.test", "key", "model", 1)

    with pytest.raises(InvalidDependencyResponse):
        await provider.generate("system", "message", uuid4())


@pytest.mark.asyncio
@respx.mock
async def test_composer_timeout_is_controlled() -> None:
    respx.post("https://composer.test/chat/completions").mock(side_effect=httpx.ReadTimeout("timeout"))
    provider = ComposerLLMProvider(httpx.AsyncClient(), "https://composer.test", "key", "model", 1)

    with pytest.raises(DependencyUnavailable):
        await provider.generate("system", "message", uuid4())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("status_code", "expected_error"),
    [(401, ComposerAuthenticationFailed), (403, ComposerAuthenticationFailed), (400, ComposerRequestRejected)],
)
@respx.mock
async def test_composer_classifies_http_errors(status_code: int, expected_error: type[Exception]) -> None:
    respx.post("https://composer.test/chat/completions").mock(
        return_value=httpx.Response(status_code, json={"error": {"message": "redacted"}})
    )
    provider = ComposerLLMProvider(httpx.AsyncClient(), "https://composer.test", "key", "model", 1)

    with pytest.raises(expected_error):
        await provider.generate("system", "message", uuid4())


def test_prompt_contains_only_allowed_context() -> None:
    prompt = build_system_prompt(ConversationContext(locale="pt-BR", resumo_sessao="resumo"), Intent.GENERAL)

    assert "pt-BR" in prompt
    assert "resumo" in prompt
    assert "CPF" not in prompt
