import random
from dataclasses import dataclass

from src.application._common.user_gateway import UserReader, UserSaver
from src.domain.entities.user import UserDTO
from src.domain.interfaces.redis import RedisGateway
from src.domain.interfaces.security import IJWTService
from src.domain.interfaces.uow import IUoW
from src.infrastructure.config import APP_DEBUG


class UserDaoGateway(UserReader, UserSaver):
    pass


@dataclass
class RegisterDTO:
    phone_number: str


async def generate_otp() -> str:
    """Generates a random 6-digit OTP."""
    return str(random.randint(100000, 999999))


class SendSmsUseCase:
    def __init__(
            self,
            user_dao: UserDaoGateway,
            redis: RedisGateway,
            jwt_service: IJWTService,
            uow: IUoW
    ):
        self._jwt_service = jwt_service
        self._user_dao = user_dao
        self._redis = redis
        self._uow = uow

    async def __call__(self, register_form: RegisterDTO, *args, **kwargs):
        db_user = await self._user_dao.get_user_by_phone_number(register_form.phone_number)
        if not db_user:
            await self._user_dao.save_user(UserDTO(phone_number=register_form.phone_number))
            await self._uow.commit()
        if APP_DEBUG:
            otp = await generate_otp()
            while await self._redis.get(otp) is not None:
                otp = await generate_otp()

            await self._redis.set(otp, register_form.phone_number, 360)
        else:
            await self._redis.set("111111", register_form.phone_number, 360)
        return {
            "detail": "The sms successfully sent.",
        }
