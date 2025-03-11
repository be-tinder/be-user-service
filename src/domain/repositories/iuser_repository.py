from abc import ABC

from src.domain.entities.user import UserDTO
from src.domain.interfaces.repository import IRepository


class IUserRepository(IRepository[UserDTO], ABC):
    async def get_user_by_number(self, phone_number: str) -> UserDTO:
        pass
