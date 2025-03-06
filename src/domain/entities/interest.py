from dataclasses import dataclass

from src.domain.interfaces.entity import BaseDTO


@dataclass
class InterestDTO(BaseDTO["Interest"]):
    id: int = None
    name: str = ""
