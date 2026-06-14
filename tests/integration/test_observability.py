import json
import logging

from autocare_agent.observability.logging import log_event


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
    event = json.loads(caplog.messages[-1])
    assert event == {"intent": "geral", "node": "completed", "request_id": "id"}
