from autocare_agent.domain.models import Intent, SessionContext
from autocare_agent.domain.protocols import SessionStore
from autocare_agent.graph.state import AgentState
from autocare_agent.observability.logging import anonymize_session


def session_nodes(store: SessionStore, ttl_seconds: int):  # type: ignore[no-untyped-def]
    async def load_session(state: AgentState) -> dict[str, object]:
        try:
            return {"session": await store.get(state["request"].sessao_id)}
        except Exception:
            return {"session": None}

    async def save_session(state: AgentState) -> dict[str, object]:
        request = state["request"]
        result = state.get("llm_result")
        intent = state.get("intent") or (result.intencao if result else Intent.UNKNOWN)
        context = SessionContext(
            sessao_hash=anonymize_session(request.sessao_id),
            resumo_sanitizado=state.get("response_text", "")[:500],
            ultima_intencao=intent,
            acoes_pendentes=state.get("actions", []),
            expires_in_seconds=ttl_seconds,
        )
        try:
            await store.set(request.sessao_id, context)
        except Exception:
            pass
        return {"session": context}

    return load_session, save_session
