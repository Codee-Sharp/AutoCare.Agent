import logging
import re
from time import perf_counter
from typing import Any, Literal, TypedDict
from uuid import UUID

from langgraph.graph import END, START, StateGraph

from autocare_agent.actions import validate_actions
from autocare_agent.llm import LLMError, LLMProvider, build_system_prompt
from autocare_agent.logging import anonymize_session, log_event
from autocare_agent.safety import (
    build_dossier,
    confirmation_question,
    detect_crisis,
    emergency_guidance,
    requests_human,
)
from autocare_agent.schemas import (
    CrisisAlert,
    HandoffDossier,
    Intent,
    LLMResult,
    ProcessRequest,
    ProcessResponse,
    ProposedAction,
)

logger = logging.getLogger("autocare_agent")
CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
Route = Literal["normal", "crisis", "ambiguous", "human", "authoritative"]


class AgentState(TypedDict, total=False):
    request: ProcessRequest
    request_id: UUID
    route: Route
    intent: Intent
    llm_result: LLMResult
    actions: list[ProposedAction]
    crisis: CrisisAlert
    handoff: HandoffDossier
    response_text: str
    response: ProcessResponse
    external_result: str


def classify_intent(message: str) -> Intent:
    lowered = message.lower()
    terms = [
        ("cancel", Intent.CANCEL),
        ("confirm", Intent.CONFIRM),
        ("desconto", Intent.DISCOUNT),
        ("serviço", Intent.SERVICE),
        ("servico", Intent.SERVICE),
        ("agendamento", Intent.LIST),
        ("horário", Intent.AVAILABILITY),
        ("horario", Intent.AVAILABILITY),
        ("disponibilidade", Intent.AVAILABILITY),
    ]
    return next((intent for term, intent in terms if term in lowered), Intent.GENERAL)


class Orchestrator:
    """Coordinates one stateless conversation through a small LangGraph."""

    def __init__(self, provider: LLMProvider, crisis_guidance_code: str) -> None:
        self.provider = provider
        self.crisis_guidance_code = crisis_guidance_code
        self.graph = self._build_graph()

    def _build_graph(self) -> Any:
        builder = StateGraph(AgentState)
        builder.add_node("sanitize_input", self._sanitize_input)
        builder.add_node("safety", self._safety)
        builder.add_node("classify_intent", self._classify_intent)
        builder.add_node("conversation", self._conversation)
        builder.add_node("validate_actions", self._validate_actions)
        builder.add_node("build_response", self._build_response)

        builder.add_edge(START, "sanitize_input")
        builder.add_edge("sanitize_input", "safety")
        builder.add_conditional_edges(
            "safety",
            self._route_after_safety,
            {
                "normal": "classify_intent",
                "crisis": "build_response",
                "ambiguous": "build_response",
                "human": "build_response",
                "authoritative": "build_response",
            },
        )
        builder.add_edge("classify_intent", "conversation")
        builder.add_edge("conversation", "validate_actions")
        builder.add_edge("validate_actions", "build_response")
        builder.add_edge("build_response", END)
        return builder.compile()

    async def process(self, request: ProcessRequest, request_id: UUID) -> ProcessResponse:
        started = perf_counter()
        result: AgentState = await self.graph.ainvoke({"request": request, "request_id": request_id})
        response = result["response"]
        log_event(
            logger,
            request_id=response.request_id,
            session_hash=anonymize_session(request.sessao_id),
            node="completed",
            intent=response.intencao,
            duration_ms=round((perf_counter() - started) * 1000, 2),
            external_result=result.get("external_result"),
            handoff_reason=response.dossie_handoff.motivo if response.dossie_handoff else None,
            crisis_reason=response.alerta_crise.tipo if response.alerta_crise else None,
        )
        return response

    def _sanitize_input(self, state: AgentState) -> dict[str, ProcessRequest]:
        request = state["request"]
        request.mensagem = CONTROL_CHARS.sub("", request.mensagem).strip()
        return {"request": request}

    def _safety(self, state: AgentState) -> AgentState:
        request = state["request"]
        crisis = detect_crisis(request.mensagem)
        if crisis.level == "crisis":
            return {
                "route": "crisis",
                "intent": Intent.CRISIS,
                "crisis": CrisisAlert(
                    tipo=crisis.category,
                    severidade="critical",
                    orientacao_codigo=self.crisis_guidance_code,
                ),
                "response_text": emergency_guidance(self.crisis_guidance_code),
                "external_result": "not_called",
            }
        if crisis.level == "ambiguous":
            return {
                "route": "ambiguous",
                "intent": Intent.CRISIS,
                "handoff": build_dossier("risco_ambiguo", Intent.CRISIS),
                "response_text": confirmation_question(),
                "external_result": "not_called",
            }
        if requests_human(request.mensagem):
            return {
                "route": "human",
                "intent": Intent.HUMAN,
                "handoff": build_dossier("pedido_explicito", Intent.HUMAN),
                "response_text": "Vou encaminhar sua solicitação para atendimento humano.",
                "external_result": "not_called",
            }

        authoritative = request.contexto.resultado_autoritativo if request.contexto else None
        if authoritative and authoritative.status == "success" and authoritative.protocolo:
            return {
                "route": "authoritative",
                "intent": Intent.GENERAL,
                "response_text": f"Operação confirmada pela aplicação interna. Protocolo: {authoritative.protocolo}",
                "external_result": "authoritative_success",
            }
        return {"route": "normal"}

    @staticmethod
    def _route_after_safety(state: AgentState) -> Route:
        return state["route"]

    @staticmethod
    def _classify_intent(state: AgentState) -> dict[str, Intent]:
        return {"intent": classify_intent(state["request"].mensagem)}

    async def _conversation(self, state: AgentState) -> AgentState:
        request = state["request"]
        intent = state["intent"]
        prompt = build_system_prompt(request.contexto, intent)
        try:
            result = await self.provider.generate(prompt, request.mensagem, state["request_id"])
            resolved_intent = result.intencao if intent == Intent.GENERAL else intent
            handoff = build_dossier("incapaz_responder", resolved_intent) if result.solicita_handoff else None
            update: AgentState = {
                "llm_result": result,
                "intent": resolved_intent,
                "response_text": result.resposta_texto,
                "external_result": "llm_success",
            }
            if handoff:
                update["handoff"] = handoff
            return update
        except LLMError as exc:
            logger.error(f"LLMError during conversation: {exc}")
            return {
                "handoff": build_dossier("falha_segura", intent),
                "response_text": "Não consigo concluir com segurança agora. Vou solicitar atendimento humano.",
                "external_result": exc.code,
            }
        except Exception as exc:
            logger.error(f"Unexpected error during conversation: {exc}")
            return {
                "handoff": build_dossier("falha_segura", intent),
                "response_text": "Não consigo concluir com segurança agora. Vou solicitar atendimento humano.",
                "external_result": "llm_failure",
            }

    @staticmethod
    def _validate_actions(state: AgentState) -> dict[str, list[ProposedAction]]:
        result = state.get("llm_result")
        actions = validate_actions(result.acoes_propostas if result else [], state["request_id"])
        return {"actions": actions}

    @staticmethod
    def _build_response(state: AgentState) -> dict[str, ProcessResponse]:
        route = state["route"]
        handoff = state.get("handoff")
        actions = state.get("actions", [])
        if handoff and actions:
            handoff = handoff.model_copy(update={"acoes_pendentes": actions})
        response = ProcessResponse(
            sucesso=route in {"normal", "human", "authoritative"} and (route != "normal" or handoff is None),
            resposta_texto=state.get("response_text", "Não foi possível responder com segurança."),
            intencao=state.get("intent", Intent.UNKNOWN),
            acoes_requeridas=actions,
            dossie_handoff=handoff,
            alerta_crise=state.get("crisis"),
            request_id=state["request_id"],
        )
        return {"response": response}
