from dishka import Provider, provide, Scope

from src.application.auth.get_profile_use_case import GetProfileUseCase
from src.application.auth.login_use_case import LoginUseCase
from src.application.auth.send_sms_use_case import SendSmsUseCase
from src.domain.interfaces.redis import RedisGateway
from src.domain.interfaces.security import IJWTService
from src.domain.interfaces.uow import IUoW
from src.infrastructure.database.dao.user_dao import UserDao


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_login_use_case(
            self,
            user_dao: UserDao,
            redis: RedisGateway,
            jwt_service: IJWTService,
    ) -> LoginUseCase:
        return LoginUseCase(user_dao=user_dao, redis=redis, jwt_service=jwt_service)

    @provide(scope=Scope.REQUEST)
    async def get_send_sms_use_case(
            self,
            user_dao: UserDao,
            redis: RedisGateway,
            jwt_service: IJWTService,
            uow: IUoW
    ) -> SendSmsUseCase:
        return SendSmsUseCase(user_dao=user_dao, redis=redis, jwt_service=jwt_service, uow=uow)

    @provide(scope=Scope.REQUEST)
    async def get_profile_use_case(
            self,
            user_dao: UserDao,
    ) -> GetProfileUseCase:
        return GetProfileUseCase(user_dao=user_dao)

