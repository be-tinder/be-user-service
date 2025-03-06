from dataclasses import dataclass, asdict
from typing import Generic, TypeVar, Type, Dict, Any

T = TypeVar('T')
M = TypeVar('M')


@dataclass
class BaseDTO(Generic[M]):
    """Base Data Transfer Object with ORM conversion methods."""

    @classmethod
    def from_orm(cls: Type[T], obj: M) -> T:
        """Convert ORM model instance to DTO."""
        fields = {f.name for f in cls.__dataclass_fields__.values()}

        values = {}
        for field_name in fields:
            if hasattr(obj, field_name):
                values[field_name] = getattr(obj, field_name)

        return cls(**values)

    def to_orm(self, model_class: Type[M]) -> M:
        """Convert DTO to ORM model instance."""
        data = asdict(self)

        filtered_data = {}
        for key, value in data.items():
            if value is not None and hasattr(model_class, key):
                filtered_data[key] = value

        return model_class(**filtered_data)

    def dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary."""
        return asdict(self)
