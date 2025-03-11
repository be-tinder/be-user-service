from typing import AsyncIterable

from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.iuser_repository import IUserRepository
from src.infrastructure.database.repositories.user_repository import UserRepository


class RepositoryIoc(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession) -> AsyncIterable[IUserRepository]:
        """Передаём в `UserRepository` уже готовую сессию (а не создаём новую)."""
        yield UserRepository(session)
