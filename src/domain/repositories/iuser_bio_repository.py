from abc import ABC

from src.domain.entities.user_bio import UserBioDTO
from src.domain.interfaces.repository import IRepository


class IUserBioRepository(IRepository[UserBioDTO], ABC):
    def get_by_user_id(self, user_id: int) -> UserBioDTO:
        pass
