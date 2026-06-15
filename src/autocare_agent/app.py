import logging
import secrets
from functools import lru_cache
from typing import Annotated
from uuid import UUID, uuid4

import httpx
from fastapi import Body, Depends, FastAPI, Request, Response, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response as StarletteResponse

from autocare_agent.config import Settings, get_settings
from autocare_agent.llm import ComposerLLMProvider
from autocare_agent.orchestrator import Orchestrator
from autocare_agent.schemas import ProcessRequest, ProcessResponse

bearer_auth = HTTPBearer(
    auto_error=False,
    scheme_name="BearerAuth",
    description="Informe somente o token configurado em APP_AUTH_TOKEN. O Swagger adicionará o prefixo Bearer.",
)

PROCESS_EXAMPLES = {
    "conversa_normal": {
        "summary": "Conversa normal - chama o Composer",
        "description": "Use este exemplo para testar o fluxo normal que chega ao Composer 2.5.",
        "value": {
            "contract_version": "1.0",
            "paciente_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sessao_id": "8c02ef48-822d-4fc3-bc33-34657c929fc7",
            "mensagem": "Olá, gostaria de conhecer os horários disponíveis.",
            "contexto": {
                "nome_preferido": "Maria",
                "locale": "pt-BR",
                "timezone": "America/Sao_Paulo",
                "resumo_sessao": "Paciente busca informações administrativas.",
            },
        },
    },
    "resultado_autoritativo": {
        "summary": "Confirmação autoritativa - não chama o Composer",
        "description": "Use somente quando a aplicação interna já executou e confirmou uma operação.",
        "value": {
            "contract_version": "1.0",
            "paciente_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "sessao_id": "8c02ef48-822d-4fc3-bc33-34657c929fc7",
            "mensagem": "A operação foi concluída?",
            "contexto": {
                "locale": "pt-BR",
                "resultado_autoritativo": {
                    "action_id": "c25185be-654c-4d45-8292-054250a7722f",
                    "status": "success",
                    "protocolo": "AG-123",
                },
            },
        },
    },
}


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> StarletteResponse:
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
                unauthorized = JSONResponse({"detail": "unauthorized", "request_id": str(request_id)}, status_code=401)
                unauthorized.headers["X-Request-ID"] = str(request_id)
                return unauthorized

        response = await call_next(request)
        response.headers["X-Request-ID"] = str(request_id)
        return response


@lru_cache
def get_orchestrator() -> Orchestrator:
    settings = get_settings()
    provider = ComposerLLMProvider(
        httpx.AsyncClient(),
        settings.composer_base_url,
        settings.composer_api_key.get_secret_value(),
        settings.composer_model,
        settings.composer_timeout_seconds,
    )
    return Orchestrator(provider, settings.crisis_guidance_code)


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    app = FastAPI(
        title="AutoCare Agent",
        version="1.0.0",
        description="Serviço stateless para processamento seguro e orquestração de conversas com LLM.",
        docs_url="/docs",
        swagger_ui_parameters={"persistAuthorization": True},
    )
    app.add_middleware(SecurityMiddleware)

    @app.post("/agent/process", response_model=ProcessResponse, tags=["agent"])
    async def process_agent(
        request: Request,
        payload: Annotated[ProcessRequest, Body(openapi_examples=PROCESS_EXAMPLES)],
        orchestrator: Orchestrator = Depends(get_orchestrator),
        runtime_settings: Settings = Depends(get_settings),
        _credentials: HTTPAuthorizationCredentials | None = Security(bearer_auth),
    ) -> ProcessResponse:
        if len(payload.mensagem) > runtime_settings.max_message_length:
            raise ValueError("mensagem exceeds configured maximum")
        return await orchestrator.process(payload, request.state.request_id)

    @app.get("/health/live", tags=["health"])
    async def live() -> dict[str, str]:
        return {"status": "live"}

    @app.get("/health/ready", tags=["health"])
    async def ready(response: Response) -> dict[str, str]:
        try:
            get_orchestrator()
        except Exception:
            response.status_code = 503
            return {"status": "not_ready"}
        return {"status": "ready"}

    @app.exception_handler(ValueError)
    async def value_error_handler(_request: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=422)

    return app


app = create_app()
