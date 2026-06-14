from typing import Protocol
from uuid import UUID

from autocare_agent.domain.models import LLMResult, SessionContext, ToolResult


class LLMProvider(Protocol):
    async def generate(self, system_prompt: str, message: str, request_id: UUID) -> LLMResult: ...


class SessionStore(Protocol):
    async def get(self, session_id: UUID) -> SessionContext | None: ...
    async def set(self, session_id: UUID, context: SessionContext) -> None: ...
    async def ping(self) -> bool: ...


class QueryTool(Protocol):
    async def call(self, paciente_id: UUID, parametros: dict[str, object], request_id: UUID) -> ToolResult: ...
