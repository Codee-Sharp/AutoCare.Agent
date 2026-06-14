from uuid import UUID

import httpx
from pydantic import ValidationError

from autocare_agent.domain.models import ToolResult, ToolStatus
from autocare_agent.tools.contracts import ToolRequest


class RestQueryClient:
    def __init__(self, client: httpx.AsyncClient, base_url: str, api_key: str, timeout: float) -> None:
        self.client = client
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    async def call(self, path: str, paciente_id: UUID, parametros: dict[str, object], request_id: UUID) -> ToolResult:
        request = ToolRequest(request_id=request_id, paciente_id=paciente_id, parametros=parametros)
        try:
            response = await self.client.post(
                f"{self.base_url}{path}",
                headers={"Authorization": f"Bearer {self.api_key}", "X-Request-ID": str(request_id)},
                json=request.model_dump(mode="json"),
                timeout=self.timeout,
            )
            response.raise_for_status()
            return ToolResult.model_validate(response.json())
        except httpx.TimeoutException:
            return ToolResult(request_id=request_id, status=ToolStatus.TIMEOUT, error_code="tool_timeout")
        except (httpx.HTTPError, ValidationError, ValueError):
            return ToolResult(request_id=request_id, status=ToolStatus.INVALID_RESPONSE, error_code="tool_invalid")
