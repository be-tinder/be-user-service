from dataclasses import dataclass

from src.domain.interfaces.entity import BaseDTO


@dataclass
class UserImageDTO(BaseDTO["UserImage"]):
    id: int = None
    image_path: str = None
    user_id: int = None
