from autocare_agent.domain.models import Intent
from autocare_agent.graph.state import AgentState
from autocare_agent.safety.dossier import build_dossier


async def create_handoff(state: AgentState) -> dict[str, object]:
    intent = state.get("intent", Intent.UNKNOWN)
    return {
        "handoff": build_dossier("pedido_explicito", intent, state.get("actions", [])),
        "response_text": "Vou encaminhar sua solicitação para atendimento humano.",
    }
