from uuid import UUID, uuid4

import pytest

from autocare_agent.llm import ComposerAuthenticationFailed
from autocare_agent.orchestrator import Orchestrator
from autocare_agent.schemas import ActionType, Intent, LLMResult, ProcessRequest, ProposedAction


class StubProvider:
    def __init__(self, result: LLMResult | None = None, error: Exception | None = None) -> None:
        self.result = result or LLMResult(resposta_texto="Resposta segura.")
        self.error = error
        self.calls = 0

    async def generate(self, system_prompt: str, message: str, request_id: UUID) -> LLMResult:
        self.calls += 1
        if self.error:
            raise self.error
        return self.result


def request(message: str) -> ProcessRequest:
    return ProcessRequest(paciente_id=uuid4(), sessao_id=uuid4(), mensagem=message)


def test_orchestrator_is_backed_by_langgraph() -> None:
    orchestrator = Orchestrator(StubProvider(), "emergency")

    assert {
        "sanitize_input",
        "safety",
        "classify_intent",
        "conversation",
        "validate_actions",
        "build_response",
    } <= set(orchestrator.graph.get_graph().nodes)


@pytest.mark.asyncio
async def test_normal_message_is_processed_by_llm() -> None:
    provider = StubProvider(LLMResult(resposta_texto="Tudo certo.", intencao=Intent.GENERAL))

    response = await Orchestrator(provider, "emergency").process(request("Olá"), uuid4())

    assert response.sucesso is True
    assert response.resposta_texto == "Tudo certo."
    assert provider.calls == 1


@pytest.mark.asyncio
async def test_crisis_interrupts_before_llm() -> None:
    provider = StubProvider()

    response = await Orchestrator(provider, "emergency").process(request("Estou pensando em suicídio"), uuid4())

    assert response.sucesso is False
    assert response.alerta_crise is not None
    assert response.alerta_crise.escalonamento_humano is True
    assert provider.calls == 0


@pytest.mark.asyncio
async def test_ambiguous_risk_interrupts_before_llm() -> None:
    provider = StubProvider()

    response = await Orchestrator(provider, "emergency").process(request("Não aguento mais"), uuid4())

    assert response.sucesso is False
    assert response.dossie_handoff is not None
    assert response.dossie_handoff.motivo == "risco_ambiguo"
    assert provider.calls == 0


@pytest.mark.asyncio
async def test_explicit_human_request_interrupts_before_llm() -> None:
    provider = StubProvider()

    response = await Orchestrator(provider, "emergency").process(request("Quero falar com um atendente"), uuid4())

    assert response.dossie_handoff is not None
    assert response.dossie_handoff.motivo == "pedido_explicito"
    assert provider.calls == 0


@pytest.mark.asyncio
async def test_llm_failure_returns_safe_handoff() -> None:
    provider = StubProvider(error=TimeoutError("timeout"))

    response = await Orchestrator(provider, "emergency").process(request("Olá"), uuid4())

    assert response.sucesso is False
    assert response.dossie_handoff is not None
    assert response.dossie_handoff.motivo == "falha_segura"


@pytest.mark.asyncio
async def test_controlled_llm_failure_is_logged_with_specific_code(caplog) -> None:
    provider = StubProvider(error=ComposerAuthenticationFailed("composer_authentication_failed"))

    with caplog.at_level("INFO"):
        await Orchestrator(provider, "emergency").process(request("Olá"), uuid4())

    assert "composer_authentication_failed" in caplog.messages[-1]


@pytest.mark.asyncio
async def test_malformed_critical_action_is_blocked() -> None:
    request_id = uuid4()
    action = ProposedAction(tipo=ActionType.CONFIRM, mode="propose", request_id=request_id)
    provider = StubProvider(LLMResult(resposta_texto="Vou verificar.", acoes_propostas=[action]))

    response = await Orchestrator(provider, "emergency").process(request("Confirmar"), request_id)

    assert response.acoes_requeridas == []


@pytest.mark.asyncio
async def test_action_from_another_request_is_blocked() -> None:
    action = ProposedAction(tipo=ActionType.AVAILABILITY, mode="query", request_id=uuid4())
    provider = StubProvider(LLMResult(resposta_texto="Vou verificar.", acoes_propostas=[action]))

    response = await Orchestrator(provider, "emergency").process(request("Horários"), uuid4())

    assert response.acoes_requeridas == []


@pytest.mark.asyncio
async def test_llm_handoff_contains_validated_pending_actions() -> None:
    request_id = uuid4()
    action = ProposedAction(tipo=ActionType.AVAILABILITY, mode="query", request_id=request_id)
    provider = StubProvider(
        LLMResult(resposta_texto="Vou transferir.", acoes_propostas=[action], solicita_handoff=True)
    )

    response = await Orchestrator(provider, "emergency").process(request("Horários"), request_id)

    assert response.sucesso is False
    assert response.dossie_handoff is not None
    assert response.dossie_handoff.acoes_pendentes == [action]
