from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.database.init_database import init_db
from src.infrastructure.di.app_provider import create_container
from src.setup_app import init_routers


def init_app():
    app = FastAPI()
    container = create_container()
    setup_dishka(container=container, app=app)

    @app.on_event("startup")
    async def on_startup():
        await init_db(await container.get(AsyncEngine))

    init_routers(app)

    return app


app = init_app()
