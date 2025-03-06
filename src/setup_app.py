from fastapi import FastAPI

from src.infrastructure.utils.autowired import DependencyContainer
from src.infrastructure.utils.import_routers import import_api_routers


def init_routers(app: FastAPI):
    routers: list = import_api_routers("src.presentation.api.routers")

    for router in routers:
        app.include_router(router, tags=router[f"{router.split('_')[0]}s"])


def register_repository():
    DependencyContainer.register()