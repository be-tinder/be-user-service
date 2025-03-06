from dataclasses import dataclass

from src.domain.interfaces.entity import BaseDTO


@dataclass
class UserBioDTO(BaseDTO["UserBio"]):
    id: int = None
    bio: str = None
    height: int = None
    goals_relation: str = None
    languages: list = None
    zodiac_sign: str = None
    education: str = None
    children_preference: str = None
    user_id: int = 0
