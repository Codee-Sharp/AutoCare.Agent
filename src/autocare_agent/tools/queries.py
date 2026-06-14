from uuid import UUID

from autocare_agent.domain.models import ToolResult
from autocare_agent.tools.client import RestQueryClient

PATHS = {
    "buscar_disponibilidade": "/tools/buscar-disponibilidade",
    "consultar_servico": "/tools/consultar-servico",
    "validar_desconto": "/tools/validar-desconto",
    "listar_agendamentos": "/tools/listar-agendamentos",
}


class QueryTools:
    def __init__(self, client: RestQueryClient) -> None:
        self.client = client

    async def call(self, name: str, paciente_id: UUID, parametros: dict[str, object], request_id: UUID) -> ToolResult:
        return await self.client.call(PATHS[name], paciente_id, parametros, request_id)
