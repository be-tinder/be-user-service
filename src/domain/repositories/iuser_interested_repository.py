from abc import ABC

from src.domain.entities.user_interested import UserInterestedDTO
from src.domain.interfaces.repository import IRepository


class IUserInterestedRepository(IRepository[UserInterestedDTO], ABC):
    def get_by_user_id(self, user_id: int) -> UserInterestedDTO:
        pass
