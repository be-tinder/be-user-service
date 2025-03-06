from fastapi import FastAPI

from src.container import AppContainer
from src.infrastructure.config import get_settings
from src.infrastructure.database.init_database import init_db
from src.presentation.api.init_routers import init_routers


def init_app():
    settings = get_settings()
    container = AppContainer()
    container.config.from_dict(
        settings.__dict__,
    )

    app = FastAPI()

    @app.on_event("startup")
    async def on_startup():
        await init_db(container.engine())
        container.initialize_use_cases()

    init_routers(app)

    return app


app = init_app()
