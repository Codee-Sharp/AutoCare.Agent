from uuid import uuid4

import httpx
import pytest
import respx

from autocare_agent.domain.errors import InvalidDependencyResponse
from autocare_agent.llm.providers import ComposerLLMProvider, FakeLLMProvider


@pytest.mark.asyncio
async def test_fake_provider_is_deterministic() -> None:
    provider = FakeLLMProvider()
    one = await provider.generate("system", "Quais horários?", uuid4())
    two = await provider.generate("system", "Quais horários?", uuid4())
    assert one.resposta_texto == two.resposta_texto
    assert one.intencao == two.intencao


@pytest.mark.asyncio
@respx.mock
async def test_composer_rejects_invalid_content() -> None:
    respx.post("https://composer.test/chat/completions").mock(
        return_value=httpx.Response(200, json={"choices": [{"message": {"content": "invalid"}}]})
    )
    provider = ComposerLLMProvider(httpx.AsyncClient(), "https://composer.test", "key", "model", 1)
    with pytest.raises(InvalidDependencyResponse):
        await provider.generate("system", "message", uuid4())
