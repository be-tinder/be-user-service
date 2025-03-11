from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from src.domain import enums
from src.domain.interfaces.entity import BaseDTO


@dataclass
class UserDTO(BaseDTO["User"]):
    """DTO for User model."""
    id: Optional[int] = None
    name: str = None
    phone_number: str = None
    email: str = None
    gender: enums.Gender = None
    sexual_orientation: str = None
    birth_date: date = None
    create_date: Optional[datetime] = None
    update_date: Optional[datetime] = None

    # user_location: Optional[UserLocationDTO] = None
    # interests: List[UserInterestDTO] = field(default_factory=list)
    # images: List[UserImageDTO] = field(default_factory=list)
    #
    # @classmethod
    # def from_orm(cls, obj: "User") -> "UserDTO":
    #     """Override from_orm to handle relationships."""
    #     instance = super().from_orm(obj)
    #
    #     if hasattr(obj, "interests") and obj.interests:
    #         instance.interests = [UserInterestDTO.from_orm(interest) for interest in obj.interests]
    #
    #     if hasattr(obj, "images") and obj.images:
    #         instance.images = [UserImageDTO.from_orm(image) for image in obj.images]
    #
    #     return instance
    #
    # def to_orm(self, model_class: Type["User"]) -> "User":
    #     """Override to_orm to handle relationships."""
    #     data = asdict(self)
    #
    #     data.pop("interests")
    #     data.pop("images")
    #     data.pop("user_location")
    #
    #     filtered_data = {}
    #     for key, value in data.items():
    #         if value is not None and hasattr(model_class, key):
    #             filtered_data[key] = value
    #
    #     user_instance = model_class(**filtered_data)
    #
    #     return user_instance
