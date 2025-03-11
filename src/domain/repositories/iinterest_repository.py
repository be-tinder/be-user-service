from abc import ABC

from src.domain.entities.interest import InterestDTO
from src.domain.interfaces.repository import IRepository


class IInterestRepository(IRepository[InterestDTO], ABC):
    pass
