from dishka import Provider, provide, Scope

from src.application.auth.login_use_case import LoginUseCase
from src.domain.interfaces.security import IJWTService
from src.domain.repositories.iuser_repository import IUserRepository


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_login_use_case(
            self,
            user_repository:
            IUserRepository,
            jwt_service: IJWTService,
    ) -> LoginUseCase:
        return LoginUseCase(user_repository, jwt_service)
