from enum import StrEnum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Intent(StrEnum):
    GENERAL = "geral"
    AVAILABILITY = "buscar_disponibilidade"
    SERVICE = "consultar_servico"
    DISCOUNT = "validar_desconto"
    CONFIRM = "confirmar_agendamento"
    LIST = "listar_agendamentos"
    CANCEL = "cancelar_agendamento"
    HUMAN = "atendimento_humano"
    CRISIS = "crise"
    UNKNOWN = "unknown"


class ActionType(StrEnum):
    AVAILABILITY = "buscar_disponibilidade"
    SERVICE = "consultar_servico"
    DISCOUNT = "validar_desconto"
    CONFIRM = "confirmar_agendamento"
    LIST = "listar_agendamentos"
    CANCEL = "cancelar_agendamento"


class AuthoritativeResult(StrictModel):
    action_id: UUID
    status: Literal["success", "rejected", "failed"]
    protocolo: str | None = Field(default=None, max_length=128)

    @model_validator(mode="after")
    def success_requires_protocol(self) -> "AuthoritativeResult":
        if self.status == "success" and not self.protocolo:
            raise ValueError("successful authoritative results require protocolo")
        return self


class ConversationContext(StrictModel):
    nome_preferido: str | None = Field(default=None, max_length=100)
    locale: str | None = Field(default=None, max_length=20)
    timezone: str | None = Field(default=None, max_length=80)
    resumo_sessao: str | None = Field(default=None, max_length=1000)
    resultado_autoritativo: AuthoritativeResult | None = None


class ProcessRequest(StrictModel):
    contract_version: Literal["1.0"] = "1.0"
    paciente_id: UUID
    sessao_id: UUID
    mensagem: str = Field(min_length=1, max_length=20000)
    contexto: ConversationContext | None = None

    @model_validator(mode="after")
    def non_blank_message(self) -> "ProcessRequest":
        self.mensagem = self.mensagem.strip()
        if not self.mensagem:
            raise ValueError("mensagem cannot be blank")
        return self


class ProposedAction(StrictModel):
    action_id: UUID = Field(default_factory=uuid4)
    tipo: ActionType
    mode: Literal["query", "propose"]
    parametros: dict[str, Any] = Field(default_factory=dict)
    request_id: UUID

    @model_validator(mode="after")
    def enforce_mode(self) -> "ProposedAction":
        critical = {ActionType.CONFIRM, ActionType.CANCEL}
        expected = "propose" if self.tipo in critical else "query"
        if self.mode != expected:
            raise ValueError(f"{self.tipo} must use mode={expected}")
        return self


class CrisisAlert(StrictModel):
    tipo: Literal["suicidio", "automutilacao", "urgencia", "violencia", "outro"]
    severidade: Literal["high", "critical"]
    orientacao_codigo: str
    escalonamento_humano: Literal[True] = True


class HandoffDossier(StrictModel):
    motivo: Literal["pedido_explicito", "falha_segura", "risco_ambiguo", "incapaz_responder"]
    intencao: Intent = Intent.UNKNOWN
    resumo_sanitizado: str = Field(max_length=500)
    acoes_pendentes: list[ProposedAction] = Field(default_factory=list)


class ProcessResponse(StrictModel):
    contract_version: Literal["1.0"] = "1.0"
    sucesso: bool
    resposta_texto: str = Field(min_length=1)
    intencao: Intent
    acoes_requeridas: list[ProposedAction] = Field(default_factory=list)
    dossie_handoff: HandoffDossier | None = None
    alerta_crise: CrisisAlert | None = None
    request_id: UUID


class LLMResult(StrictModel):
    resposta_texto: str = Field(min_length=1, max_length=4000)
    intencao: Intent = Intent.GENERAL
    acoes_propostas: list[ProposedAction] = Field(default_factory=list, max_length=10)
    solicita_handoff: bool = False
