from typing import Dict, Any

from src.domain.interfaces.use_case import IBaseUseCase
from src.domain.repositories.iuser_repository import IUserRepository


class UserRetrieveUseCase(IBaseUseCase):
    __for_service__ = "user_retrieve"

    def __init__(self, user_repository: IUserRepository, **kwargs):
        super().__init__(user_repository, **kwargs)
        self._user_repository = user_repository

    async def execute(self, user_id: int) -> Dict[str, Any]:
        """Retrieve a user by ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing user details or an error message.
        """
        if not user_id:
            return {"error": "User ID is required", "status_code": 400}

        user = await self._user_repository.get_by_id(user_id)

        if not user:
            return {"error": "User not found", "status_code": 404}

        return user.dict()
