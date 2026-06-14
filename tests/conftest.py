import os
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

# Automated tests must remain deterministic and independent of the developer's .env.
os.environ["COMPOSER_API_KEY"] = "test-api-key"

from autocare_agent.app import app, get_orchestrator
from autocare_agent.orchestrator import Orchestrator
from autocare_agent.schemas import Intent, LLMResult


class StubLLMProvider:
    async def generate(self, system_prompt: str, message: str, request_id: UUID) -> LLMResult:
        lowered = message.lower()
        intent = Intent.AVAILABILITY if "horário" in lowered or "disponibilidade" in lowered else Intent.GENERAL
        return LLMResult(resposta_texto="Posso ajudar com essa solicitação administrativa.", intencao=intent)


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[get_orchestrator] = lambda: Orchestrator(StubLLMProvider(), "contact_emergency_services")
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"Authorization": "Bearer local-development-token", "X-Request-ID": str(uuid4())}


@pytest.fixture
def process_payload() -> dict[str, object]:
    return {
        "contract_version": "1.0",
        "paciente_id": str(uuid4()),
        "sessao_id": str(uuid4()),
        "mensagem": "Olá, preciso de ajuda administrativa.",
        "contexto": {"locale": "pt-BR", "timezone": "America/Sao_Paulo"},
    }
