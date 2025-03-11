from fastapi import HTTPException

from src.domain.entities.user import UserDTO
from src.domain.interfaces.security import IJWTService
from src.domain.repositories.iuser_repository import IUserRepository


class LoginUseCase:
    def __init__(
            self,
            user_repository: IUserRepository,
            jwt_service: IJWTService,
    ):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def execute(self, user: UserDTO):
        db_user = await self.user_repository.get_by_id(user.id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        access_token = self.jwt_service.encode_jwt(user_id=db_user.id, is_refresh=False)
        refresh_token = self.jwt_service.encode_jwt(user_id=db_user.id, is_refresh=True)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
