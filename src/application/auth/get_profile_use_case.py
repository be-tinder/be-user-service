from src.application._common.user_gateway import UserReader
from src.domain.exceptions import DomainError


class UserDaoGateway(UserReader):
    pass


class GetProfileUseCase:
    def __init__(
            self,
            user_dao: UserDaoGateway,
    ):
        self._user_dao = user_dao

    async def __call__(self, user_id: int, *args, **kwargs):
        db_user = await self._user_dao.get_user_by_id(user_id)
        if not db_user:
            raise DomainError({"detail": "User not found"})

        return db_user
