import json
import logging
from uuid import uuid4

from autocare_agent.logging import anonymize_session, log_event, safe_event


def test_logging_uses_allowlist() -> None:
    event = safe_event(request_id="id", node="test", mensagem="segredo", cpf="123")

    assert event == {"request_id": "id", "node": "test"}
    assert anonymize_session(uuid4()) != anonymize_session(uuid4())


def test_structured_logs_exclude_sensitive_fields(caplog) -> None:
    with caplog.at_level(logging.INFO):
        log_event(
            logging.getLogger("test"),
            request_id="id",
            node="completed",
            intent="geral",
            mensagem="conteúdo secreto",
            cpf="123",
        )

    assert json.loads(caplog.messages[-1]) == {"intent": "geral", "node": "completed", "request_id": "id"}
