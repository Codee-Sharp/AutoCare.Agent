from uuid import UUID

from pydantic import ValidationError

from autocare_agent.schemas import ActionType, ProposedAction, StrictModel


class ConfirmParams(StrictModel):
    servico_id: UUID
    slot_id: UUID


class CancelParams(StrictModel):
    agendamento_id: UUID


def validate_actions(actions: list[ProposedAction], request_id: UUID) -> list[ProposedAction]:
    """Keep only actions that belong to this request and have safe critical payloads."""

    validated: list[ProposedAction] = []
    for action in actions:
        if action.request_id != request_id:
            continue
        try:
            if action.tipo == ActionType.CONFIRM:
                ConfirmParams.model_validate(action.parametros)
            elif action.tipo == ActionType.CANCEL:
                CancelParams.model_validate(action.parametros)
        except ValidationError:
            continue
        validated.append(action)
    return validated
