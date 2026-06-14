from pydantic import ValidationError

from autocare_agent.domain.models import ActionType, ProposedAction
from autocare_agent.tools.contracts import CancelParams, ConfirmParams


def validate_actions(actions: list[ProposedAction]) -> list[ProposedAction]:
    validated: list[ProposedAction] = []
    for action in actions:
        try:
            if action.tipo == ActionType.CONFIRM:
                ConfirmParams.model_validate(action.parametros)
            elif action.tipo == ActionType.CANCEL:
                CancelParams.model_validate(action.parametros)
            validated.append(action)
        except ValidationError:
            continue
    return validated
