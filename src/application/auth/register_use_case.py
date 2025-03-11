from src.domain.entities.user import UserDTO
from src.domain.repositories.iuser_repository import IUserRepository


class RegisterUseCase:
    def __init__(
            self,
            user_repository: IUserRepository,
    ):
        self.user_repository = user_repository

    async def execute(self, user: UserDTO):
        db_user = await self.user_repository.get_user_by_number(user.phone_number)
        if db_user:
            raise

        await self.user_repository.add(user)
        return user
