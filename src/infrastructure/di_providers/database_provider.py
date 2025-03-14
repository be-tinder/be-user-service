from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.domain.interfaces.redis import RedisGateway
from src.domain.interfaces.uow import IUoW
from src.infrastructure.cache.redis_client import RedisClient
from src.infrastructure.cache.redis_manager import RedisManager
from src.infrastructure.config import Settings
from src.infrastructure.database.alchemy_config import create_engine, create_session
from src.infrastructure.database.uow import UoW


class DatabaseIoc(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        """Provides application settings."""
        return Settings()

    @provide(scope=Scope.APP)
    async def get_engine(self, settings: Settings) -> AsyncIterable[AsyncEngine]:
        """Создаём движок SQLAlchemy."""
        engine = await create_engine(settings.async_db_url)
        try:
            yield engine
        finally:
            await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        """Создаём фабрику сессий."""
        return await create_session(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_uow(self, session: AsyncSession) -> IUoW:
        return UoW(session)

    @provide(scope=Scope.APP)
    async def get_redis_client(self, settings: Settings) -> RedisClient:
        return RedisClient(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    @provide(scope=Scope.REQUEST)
    async def get_redis_manager(self, redis: RedisClient) -> RedisGateway:
        return RedisManager(redis.get_client())
