from dataclasses import dataclass
from typing import Literal, cast

from autocare_agent.schemas import HandoffDossier, Intent, ProposedAction


@dataclass(frozen=True)
class CrisisDetection:
    level: Literal["none", "ambiguous", "crisis"]
    category: Literal["suicidio", "automutilacao", "urgencia", "violencia", "outro"] = "outro"


CRISIS_TERMS = {
    "suicidio",
    "suicídio",
    "me matar",
    "automutilacao",
    "automutilação",
    "emergencia",
    "emergência",
}
AMBIGUOUS_TERMS = {"nao aguento", "não aguento", "desespero", "sumir", "sem saida", "sem saída"}
HUMAN_TERMS = {"atendente", "humano", "pessoa", "falar com alguem", "falar com alguém"}


def detect_crisis(message: str) -> CrisisDetection:
    lowered = message.lower()
    if any(term in lowered for term in CRISIS_TERMS):
        category = "suicidio" if "suic" in lowered or "me matar" in lowered else "urgencia"
        return CrisisDetection("crisis", cast("Literal['suicidio', 'urgencia']", category))
    if any(term in lowered for term in AMBIGUOUS_TERMS):
        return CrisisDetection("ambiguous")
    return CrisisDetection("none")


def requests_human(message: str) -> bool:
    lowered = message.lower()
    return any(term in lowered for term in HUMAN_TERMS)


def emergency_guidance(code: str) -> str:
    return (
        "Sua segurança é prioridade. Procure imediatamente os serviços de emergência "
        f"da sua região e aguarde atendimento humano. Referência: {code}."
    )


def confirmation_question() -> str:
    return "Você está em risco imediato ou pensando em se machucar agora?"


def build_dossier(
    reason: Literal["pedido_explicito", "falha_segura", "risco_ambiguo", "incapaz_responder"],
    intent: Intent,
    actions: list[ProposedAction] | None = None,
) -> HandoffDossier:
    return HandoffDossier(
        motivo=reason,
        intencao=intent,
        resumo_sanitizado=f"Transferência solicitada. Motivo: {reason}.",
        acoes_pendentes=actions or [],
    )
