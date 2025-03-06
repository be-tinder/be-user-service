from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any, Type

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    _subclasses: Dict[str, Type["IRepository"]] = {}

    def __init_subclass__(cls, **kwargs):
        """Automatically registers subclasses when they are defined."""
        super().__init_subclass__(**kwargs)
        IRepository._subclasses[cls.__name__] = cls

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve a single entity by its identifier."""
        pass

    @abstractmethod
    async def list(self, filters: Optional[Dict[str, Any]] = None) -> List[T]:
        """Retrieve all entities matching the optional filters."""
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add a new entity to the repository."""
        pass

    @abstractmethod
    async def remove(self, id: int) -> bool:
        """Remove an entity from the repository."""
        pass

    @abstractmethod
    async def update(self, id: int, entity: T) -> T:
        """Update an existing entity."""
        pass
