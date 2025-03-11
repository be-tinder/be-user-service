from typing import Dict, Any

from fastapi import FastAPI

from src.infrastructure.utils.import_routers import import_api_routers


def init_routers(app: FastAPI):
    routers: list[Dict[str, Any]] = import_api_routers("src.presentation.api.routers")
    for router in routers:
        tag = router["module"].split("_")[0]
        app.include_router(router["router"], tags=[tag])
