from autocare_agent.domain.models import Intent, ProcessResponse
from autocare_agent.graph.state import AgentState


async def build_response(state: AgentState) -> dict[str, object]:
    request = state["request"]
    authoritative = request.contexto.resultado_autoritativo if request.contexto else None
    authoritative_success = bool(authoritative and authoritative.status == "success" and authoritative.protocolo)
    response = ProcessResponse(
        sucesso=not state.get("safe_failure", False) and state.get("crisis") is None,
        resposta_texto=state.get("response_text", "Não foi possível responder com segurança."),
        intencao=state.get("intent", Intent.UNKNOWN),
        acoes_requeridas=state.get("actions", []),
        dossie_handoff=state.get("handoff"),
        alerta_crise=state.get("crisis"),
        request_id=state["request_id"],
    )
    if authoritative_success and authoritative is not None:
        response.sucesso = True
        response.resposta_texto = f"Operação confirmada pela aplicação interna. Protocolo: {authoritative.protocolo}"
    return {"response": response}
