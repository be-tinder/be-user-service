from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncEngine

from src.handlers import init_routers, handle_errors, init_middlewares
from src.infrastructure.database.init_database import init_db
from src.infrastructure.di_providers.app_provider import create_container

token = HTTPBearer()


def init_app():
    app = FastAPI()
    container = create_container()
    setup_dishka(container=container, app=app)

    @app.on_event("startup")
    async def on_startup():
        await init_db(await container.get(AsyncEngine))

    init_routers(app)
    handle_errors(app)
    # init_middlewares(app, container)

    return app


app = init_app()
