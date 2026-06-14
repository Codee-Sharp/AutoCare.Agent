from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from autocare_agent.api.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


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
