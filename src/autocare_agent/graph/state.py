from typing import Any, TypedDict
from uuid import UUID

from autocare_agent.domain.models import (
    CrisisAlert,
    HandoffDossier,
    Intent,
    LLMResult,
    ProcessRequest,
    ProcessResponse,
    ProposedAction,
    SessionContext,
)


class AgentState(TypedDict, total=False):
    request: ProcessRequest
    request_id: UUID
    session: SessionContext | None
    intent: Intent
    prompt: str
    llm_result: LLMResult
    actions: list[ProposedAction]
    crisis: CrisisAlert
    handoff: HandoffDossier
    safe_failure: bool
    response_text: str
    response: ProcessResponse
    route: str
    metadata: dict[str, Any]
