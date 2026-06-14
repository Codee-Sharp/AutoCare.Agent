from uuid import uuid4

from autocare_agent.observability.logging import anonymize_session, safe_event


def test_logging_uses_allowlist() -> None:
    event = safe_event(request_id="id", node="test", mensagem="segredo", cpf="123")
    assert event == {"request_id": "id", "node": "test"}
    assert anonymize_session(uuid4()) != anonymize_session(uuid4())
