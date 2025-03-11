from dataclasses import dataclass

from src.domain.interfaces.entity import BaseDTO


@dataclass
class UserLocationDTO(BaseDTO["UserLocation"]):
    id: int = None
    latitude: float = None
    longitude: float = None
    user_id: int = None
