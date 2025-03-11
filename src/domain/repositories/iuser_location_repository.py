from abc import ABC

from src.domain.entities.user_location import UserLocationDTO
from src.domain.interfaces.repository import IRepository


class IUserLocationRepository(IRepository[UserLocationDTO], ABC):
    def get_by_user_id(self, user_id: int) -> UserLocationDTO:
        pass
