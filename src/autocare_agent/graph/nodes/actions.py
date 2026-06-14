from autocare_agent.domain.models import ActionType, Intent, ProposedAction
from autocare_agent.graph.state import AgentState
from autocare_agent.tools.validator import validate_actions


async def validate_action_node(state: AgentState) -> dict[str, object]:
    result = state.get("llm_result")
    actions = validate_actions(result.acoes_propostas if result else [])
    intent = state.get("intent", Intent.GENERAL)
    request_id = state["request_id"]
    if not actions and intent in {Intent.CONFIRM, Intent.CANCEL}:
        action_type = ActionType.CONFIRM if intent == Intent.CONFIRM else ActionType.CANCEL
        actions = [ProposedAction(tipo=action_type, mode="propose", parametros={}, request_id=request_id)]
    return {"actions": actions}
