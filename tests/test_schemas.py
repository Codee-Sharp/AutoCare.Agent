from uuid import uuid4

import pytest
from pydantic import ValidationError

from autocare_agent.schemas import ActionType, AuthoritativeResult, ProcessRequest, ProposedAction


def test_forbids_extra_patient_fields() -> None:
    with pytest.raises(ValidationError):
        ProcessRequest(
            paciente_id=uuid4(),
            sessao_id=uuid4(),
            mensagem="oi",
            contexto={"cpf": "123"},  # type: ignore[arg-type]
        )


def test_success_requires_authoritative_protocol() -> None:
    with pytest.raises(ValidationError):
        AuthoritativeResult(action_id=uuid4(), status="success")


def test_critical_action_must_be_proposal() -> None:
    with pytest.raises(ValidationError):
        ProposedAction(tipo=ActionType.CONFIRM, mode="query", request_id=uuid4())
