from autocare_agent.domain.models import Intent
from autocare_agent.domain.protocols import LLMProvider
from autocare_agent.graph.state import AgentState
from autocare_agent.llm.prompt_builder import build_system_prompt
from autocare_agent.safety.dossier import build_dossier


def conversation_node(provider: LLMProvider):  # type: ignore[no-untyped-def]
    async def converse(state: AgentState) -> dict[str, object]:
        request = state["request"]
        intent = state.get("intent", Intent.GENERAL)
        prompt = build_system_prompt(request.contexto, intent)
        try:
            result = await provider.generate(prompt, request.mensagem, state["request_id"])
            return {"prompt": prompt, "llm_result": result, "response_text": result.resposta_texto}
        except Exception:
            return {
                "safe_failure": True,
                "handoff": build_dossier("falha_segura", intent),
                "response_text": "Não consigo concluir com segurança agora. Vou solicitar atendimento humano.",
            }

    return converse
