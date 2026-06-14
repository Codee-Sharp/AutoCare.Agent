from uuid import UUID

from autocare_agent.domain.models import ActionType, ProposedAction


def propose_confirmation(request_id: UUID, parametros: dict[str, object]) -> ProposedAction:
    return ProposedAction(tipo=ActionType.CONFIRM, mode="propose", parametros=parametros, request_id=request_id)


def propose_cancellation(request_id: UUID, parametros: dict[str, object]) -> ProposedAction:
    return ProposedAction(tipo=ActionType.CANCEL, mode="propose", parametros=parametros, request_id=request_id)
