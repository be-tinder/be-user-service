from typing import AsyncIterable

from dishka import Provider, Scope, provide

from src.application.users.user_retrieve_case import UserRetrieveUseCase
from src.domain.repositories.iuser_repository import IUserRepository


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_user_retrieve_use_case(self, user_repository: IUserRepository) -> AsyncIterable[UserRetrieveUseCase]:
        yield UserRetrieveUseCase(user_repository)
