from dataclasses import dataclass

from src.domain.entities.user import UserDTO


@dataclass
class UserImageDTO(UserDTO["UserImage"]):
    id: int = None
    image_path: str = None
    user_id: int = None
