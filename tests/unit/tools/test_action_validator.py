from uuid import uuid4

from autocare_agent.domain.models import ActionType, ProposedAction
from autocare_agent.tools.validator import validate_actions


def test_blocks_malformed_critical_action() -> None:
    action = ProposedAction(tipo=ActionType.CONFIRM, mode="propose", request_id=uuid4())
    assert validate_actions([action]) == []
