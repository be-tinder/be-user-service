from abc import ABC, abstractmethod
from typing import Type, Dict, Any, Optional

from src.domain.interfaces.uow import IUoW
from src.domain.interfaces.repository import IRepository


class IBaseUseCase(ABC):
    __for_service__ = ""
    subclasses: Dict[str, Type["IBaseUseCase"]] = {}

    def __init__(self, repository: IRepository, uow: IUoW, **kwargs):
        self.repository = repository
        self.uow = uow
        self.kwargs = kwargs

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """Asynchronous method to be implemented in subclasses."""
        pass

    def __init_subclass__(cls, **kwargs):
        """Automatically registers subclasses when they are defined."""
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__for_service__] = cls

    @classmethod
    def get_sub_class(cls, service_name: str) -> Optional[Type["IRepository"]]:
        """Retrieves a registered repository subclass by name."""
        return cls.subclasses.get(service_name)
