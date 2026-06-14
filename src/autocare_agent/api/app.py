import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from autocare_agent.api.middleware import SecurityMiddleware
from autocare_agent.api.routes.agent import router as agent_router
from autocare_agent.api.routes.health import router as health_router
from autocare_agent.config.settings import get_settings


def create_app() -> FastAPI:
    logging.basicConfig(level=get_settings().log_level)
    app = FastAPI(title="AutoCare Agent", version="1.0.0")
    app.add_middleware(SecurityMiddleware)
    app.include_router(agent_router)
    app.include_router(health_router)

    @app.exception_handler(ValueError)
    async def value_error_handler(_request: object, exc: ValueError) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=422)

    return app


app = create_app()
