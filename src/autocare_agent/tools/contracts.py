from typing import Any, Literal
from uuid import UUID

from pydantic import Field

from autocare_agent.domain.models import StrictModel


class ToolRequest(StrictModel):
    contract_version: Literal["1.0"] = "1.0"
    request_id: UUID
    paciente_id: UUID
    parametros: dict[str, Any] = Field(default_factory=dict)


class AvailabilityParams(StrictModel):
    servico_id: UUID | None = None
    data_inicio: str | None = None
    data_fim: str | None = None


class ServiceParams(StrictModel):
    servico_id: UUID | None = None
    termo: str | None = None


class DiscountParams(StrictModel):
    servico_id: UUID


class AppointmentListParams(StrictModel):
    status: str | None = None


class ConfirmParams(StrictModel):
    servico_id: UUID
    slot_id: UUID


class CancelParams(StrictModel):
    agendamento_id: UUID
