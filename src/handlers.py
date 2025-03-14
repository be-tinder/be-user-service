from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer
from starlette.responses import JSONResponse

from src.domain.exceptions import BaseError
from src.infrastructure.import_routers import import_api_routers
from src.presentation.api.middlewares import AuthMiddleware


def init_routers(app: FastAPI):
    routers: list[Dict[str, Any]] = import_api_routers("src.presentation.api.routers")
    for router in routers:
        tag = router["module"].split("_")[0]
        app.include_router(router["router"], tags=[tag])


def handle_errors(app: FastAPI):
    @app.exception_handler(BaseError)
    def handle_base_error(request: Request, exc: BaseError):
        return JSONResponse({"error": str(exc)}, status_code=exc.status_code)


def init_middlewares(app: FastAPI, container):
    app.add_middleware(
        AuthMiddleware,
        container=container,
        allowed_paths=['/docs', '/send-otp']
    )
