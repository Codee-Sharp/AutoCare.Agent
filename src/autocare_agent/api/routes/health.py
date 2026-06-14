from fastapi import APIRouter, Depends, Response

from autocare_agent.api.dependencies import get_session_store
from autocare_agent.domain.protocols import SessionStore

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def live() -> dict[str, str]:
    return {"status": "live"}


@router.get("/ready")
async def ready(response: Response, store: SessionStore = Depends(get_session_store)) -> dict[str, str]:
    try:
        is_ready = await store.ping()
    except Exception:
        is_ready = False
    if not is_ready:
        response.status_code = 503
        return {"status": "not_ready"}
    return {"status": "ready"}
