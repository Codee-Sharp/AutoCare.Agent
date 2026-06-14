from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class CrisisDetection:
    level: Literal["none", "ambiguous", "crisis"]
    category: str = "outro"


CRISIS_TERMS = {"suicídio", "suicidio", "me matar", "automutilação", "automutilacao", "emergência", "emergencia"}
AMBIGUOUS_TERMS = {"não aguento", "nao aguento", "desespero", "sumir", "sem saída", "sem saida"}


def detect_crisis(message: str) -> CrisisDetection:
    lowered = message.lower()
    if any(term in lowered for term in CRISIS_TERMS):
        category = "suicidio" if "suic" in lowered or "me matar" in lowered else "urgencia"
        return CrisisDetection("crisis", category)
    if any(term in lowered for term in AMBIGUOUS_TERMS):
        return CrisisDetection("ambiguous")
    return CrisisDetection("none")
