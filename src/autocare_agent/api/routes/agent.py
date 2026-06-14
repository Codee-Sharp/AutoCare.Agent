from fastapi import APIRouter, Depends, Request

from autocare_agent.api.dependencies import get_workflow
from autocare_agent.config.settings import get_settings
from autocare_agent.domain.models import ProcessRequest, ProcessResponse
from autocare_agent.graph.workflow import Workflow

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/process", response_model=ProcessResponse)
async def process_agent(
    request: Request,
    payload: ProcessRequest,
    workflow: Workflow = Depends(get_workflow),
) -> ProcessResponse:
    if len(payload.mensagem) > get_settings().max_message_length:
        raise ValueError("mensagem exceeds configured maximum")
    return await workflow.process(payload, request.state.request_id)
