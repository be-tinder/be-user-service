from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.dao.user_dao import UserDao


class DAOProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_user_dao(self, session: AsyncSession) -> UserDao:
        return UserDao(session)