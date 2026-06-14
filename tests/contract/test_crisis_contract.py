from uuid import uuid4

from autocare_agent.domain.models import CrisisAlert, ProcessResponse


def test_crisis_contract_has_no_message_content() -> None:
    response = ProcessResponse(
        sucesso=False,
        resposta_texto="orientação segura",
        intencao="crise",
        alerta_crise=CrisisAlert(tipo="urgencia", severidade="critical", orientacao_codigo="emergency"),
        request_id=uuid4(),
    )
    assert "mensagem" not in response.model_dump()["alerta_crise"]
