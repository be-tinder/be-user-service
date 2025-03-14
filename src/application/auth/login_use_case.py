from dataclasses import dataclass

from src.application._common.user_gateway import UserReader
from src.domain.exceptions import AuthError
from src.domain.interfaces.redis import RedisGateway
from src.domain.interfaces.security import IJWTService


class UserDaoGateway(UserReader):
    pass


@dataclass
class LoginDTO:
    phone_number: str
    otp_code: str


class LoginUseCase:
    def __init__(
            self,
            user_dao: UserDaoGateway,
            redis: RedisGateway,
            jwt_service: IJWTService,
    ):
        self._jwt_service = jwt_service
        self._user_dao = user_dao
        self._redis = redis

    async def __call__(self, login_form: LoginDTO, *args, **kwargs):
        db_user = await self._user_dao.get_user_by_phone_number(login_form.phone_number)
        if not db_user:
            raise AuthError("User not found")

        stored_otp = await self._redis.get(login_form.otp_code)

        if not stored_otp:
            raise AuthError("OTP code not found")

        access_token = self._jwt_service.encode_jwt(db_user.id, is_refresh=False)
        refresh_token = self._jwt_service.encode_jwt(db_user.id, is_refresh=True)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
