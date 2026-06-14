import logging
from dataclasses import dataclass
from uuid import UUID

from langgraph.graph import END, START, StateGraph

from autocare_agent.domain.models import ProcessRequest, ProcessResponse
from autocare_agent.domain.protocols import LLMProvider, SessionStore
from autocare_agent.graph.nodes.actions import validate_action_node
from autocare_agent.graph.nodes.conversation import conversation_node
from autocare_agent.graph.nodes.crisis import crisis_node
from autocare_agent.graph.nodes.handoff import create_handoff
from autocare_agent.graph.nodes.input_validation import validate_input
from autocare_agent.graph.nodes.intent import classify_intent
from autocare_agent.graph.nodes.response import build_response
from autocare_agent.graph.nodes.session_context import session_nodes
from autocare_agent.graph.state import AgentState
from autocare_agent.observability.logging import anonymize_session, log_event

logger = logging.getLogger("autocare_agent")


@dataclass
class Workflow:
    graph: object

    async def process(self, request: ProcessRequest, request_id: UUID) -> ProcessResponse:
        result = await self.graph.ainvoke({"request": request, "request_id": request_id})  # type: ignore[attr-defined]
        response: ProcessResponse = result["response"]
        return response


def build_workflow(provider: LLMProvider, store: SessionStore, ttl_seconds: int, guidance_code: str) -> Workflow:
    load_session, save_session = session_nodes(store, ttl_seconds)
    builder = StateGraph(AgentState)
    builder.add_node("validate_input", validate_input)
    builder.add_node("load_session", load_session)
    builder.add_node("detect_crisis", crisis_node(guidance_code))
    builder.add_node("classify_intent", classify_intent)
    builder.add_node("handoff", create_handoff)
    builder.add_node("conversation", conversation_node(provider))
    builder.add_node("validate_actions", validate_action_node)
    builder.add_node("save_session", save_session)
    builder.add_node("build_response", build_response)
    builder.add_edge(START, "validate_input")
    builder.add_edge("validate_input", "load_session")
    builder.add_edge("load_session", "detect_crisis")
    builder.add_conditional_edges(
        "detect_crisis",
        lambda state: state.get("route", "normal"),
        {"crisis": "build_response", "ambiguous": "build_response", "normal": "classify_intent"},
    )
    builder.add_conditional_edges(
        "classify_intent",
        lambda state: state.get("route", "normal"),
        {"human": "handoff", "normal": "conversation"},
    )
    builder.add_edge("handoff", "build_response")
    builder.add_edge("conversation", "validate_actions")
    builder.add_edge("validate_actions", "save_session")
    builder.add_edge("save_session", "build_response")
    builder.add_edge("build_response", END)
    compiled = builder.compile()

    original_process = Workflow(compiled).process

    async def observed_process(request: ProcessRequest, request_id: UUID) -> ProcessResponse:
        response = await original_process(request, request_id)
        log_event(
            logger,
            request_id=request_id,
            session_hash=anonymize_session(request.sessao_id),
            node="completed",
            intent=response.intencao,
            handoff_reason=response.dossie_handoff.motivo if response.dossie_handoff else None,
            crisis_reason=response.alerta_crise.tipo if response.alerta_crise else None,
        )
        return response

    workflow = Workflow(compiled)
    workflow.process = observed_process  # type: ignore[method-assign]
    return workflow
