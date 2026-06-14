from autocare_agent.domain.models import Intent
from autocare_agent.graph.state import AgentState
from autocare_agent.safety.handoff import requests_human


async def classify_intent(state: AgentState) -> dict[str, object]:
    message = state["request"].mensagem.lower()
    if requests_human(message):
        return {"intent": Intent.HUMAN, "route": "human"}
    terms = [
        ("cancel", Intent.CANCEL),
        ("confirm", Intent.CONFIRM),
        ("desconto", Intent.DISCOUNT),
        ("serviço", Intent.SERVICE),
        ("servico", Intent.SERVICE),
        ("agendamento", Intent.LIST),
        ("horário", Intent.AVAILABILITY),
        ("horario", Intent.AVAILABILITY),
    ]
    for term, intent in terms:
        if term in message:
            return {"intent": intent}
    return {"intent": Intent.GENERAL}
