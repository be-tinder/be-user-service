from abc import ABC

from src.domain.entities.user_image import UserImageDTO
from src.domain.interfaces.repository import IRepository


class IUserImagesRepository(IRepository[UserImageDTO], ABC):
    def get_by_user_id(self, user_id: int) -> UserImageDTO:
        pass