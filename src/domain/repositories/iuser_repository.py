from abc import ABC

from src.domain.entities.user import UserDTO
from src.domain.interfaces.repository import IRepository


class IUserRepository(IRepository[UserDTO], ABC):
    pass