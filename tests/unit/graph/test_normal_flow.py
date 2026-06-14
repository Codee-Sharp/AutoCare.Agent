from uuid import uuid4

import pytest

from autocare_agent.domain.models import ProcessRequest
from autocare_agent.graph.workflow import build_workflow
from autocare_agent.llm.providers import FakeLLMProvider
from autocare_agent.session.store import InMemorySessionStore


@pytest.mark.asyncio
async def test_normal_graph_persists_sanitized_session_context() -> None:
    store = InMemorySessionStore()
    workflow = build_workflow(FakeLLMProvider(), store, 1800, "emergency")
    request = ProcessRequest(paciente_id=uuid4(), sessao_id=uuid4(), mensagem="Quero horários")

    response = await workflow.process(request, uuid4())

    assert response.sucesso
    context = await store.get(request.sessao_id)
    assert context is not None
    assert request.mensagem not in context.resumo_sanitizado
