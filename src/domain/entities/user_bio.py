from dataclasses import dataclass
from typing import List

from src.domain.interfaces.entity import BaseDTO


@dataclass
class UserBioDTO(BaseDTO["UserBio"]):
    id: int = None
    bio: str = None
    height: int = None
    goals_relation: str = None
    languages: List[str] = None
    zodiac_sign: str = None
    education: str = None
    children_preference: str = None
    user_id: int = None
