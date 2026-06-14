from uuid import uuid4

from autocare_agent.actions import validate_actions
from autocare_agent.schemas import ActionType, ProposedAction


def test_valid_critical_action_is_kept_as_proposal() -> None:
    request_id = uuid4()
    action = ProposedAction(
        tipo=ActionType.CONFIRM,
        mode="propose",
        request_id=request_id,
        parametros={"servico_id": str(uuid4()), "slot_id": str(uuid4())},
    )

    assert validate_actions([action], request_id) == [action]


def test_malformed_critical_action_is_blocked() -> None:
    request_id = uuid4()
    action = ProposedAction(tipo=ActionType.CANCEL, mode="propose", request_id=request_id)

    assert validate_actions([action], request_id) == []
