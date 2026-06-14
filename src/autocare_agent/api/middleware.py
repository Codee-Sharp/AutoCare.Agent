import secrets
from uuid import UUID, uuid4

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from autocare_agent.config.settings import get_settings


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        raw_id = request.headers.get("X-Request-ID")
        try:
            request_id = UUID(raw_id) if raw_id else uuid4()
        except ValueError:
            request_id = uuid4()
        request.state.request_id = request_id
        if request.url.path.startswith("/agent/"):
            expected = get_settings().app_auth_token.get_secret_value()
            received = request.headers.get("Authorization", "").removeprefix("Bearer ")
            if not secrets.compare_digest(received, expected):
                return JSONResponse({"detail": "unauthorized", "request_id": str(request_id)}, status_code=401)
        response = await call_next(request)
        response.headers["X-Request-ID"] = str(request_id)
        return response
