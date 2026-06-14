from autocare_agent.domain.models import CrisisAlert, Intent
from autocare_agent.graph.state import AgentState
from autocare_agent.safety.crisis import detect_crisis
from autocare_agent.safety.dossier import build_dossier
from autocare_agent.safety.guidance import confirmation_question, emergency_guidance


def crisis_node(guidance_code: str):  # type: ignore[no-untyped-def]
    async def detect(state: AgentState) -> dict[str, object]:
        result = detect_crisis(state["request"].mensagem)
        if result.level == "crisis":
            return {
                "intent": Intent.CRISIS,
                "crisis": CrisisAlert(
                    tipo=result.category,  # type: ignore[arg-type]
                    severidade="critical",
                    orientacao_codigo=guidance_code,
                ),
                "response_text": emergency_guidance(guidance_code),
                "route": "crisis",
            }
        if result.level == "ambiguous":
            return {
                "intent": Intent.CRISIS,
                "handoff": build_dossier("risco_ambiguo", Intent.CRISIS),
                "response_text": confirmation_question(),
                "route": "ambiguous",
            }
        return {"route": "normal"}

    return detect
