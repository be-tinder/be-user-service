from dataclasses import dataclass, asdict
from typing import Generic, TypeVar, Type, Dict, Any

T = TypeVar("T")  # DTO type
M = TypeVar("M")  # ORM model type


@dataclass
class BaseDTO(Generic[M]):
    """
    Base Data Transfer Object with generic ORM conversion methods.
    """

    @classmethod
    def from_orm(cls: Type[T], obj: M) -> T:
        """
        Convert an ORM model instance to a DTO.
        """
        fields = {f.name for f in cls.__dataclass_fields__.values()}
        values = {}
        for field_name in fields:
            if hasattr(obj, field_name):
                values[field_name] = getattr(obj, field_name)
        return cls(**values)

    def to_orm(self, model_class: Type[M]) -> M:
        """
        Convert a DTO instance to an ORM model instance.
        By default, this ignores any fields that are None
        or that do not exist on the model class.
        """
        data = asdict(self)
        filtered_data = {}
        for key, value in data.items():
            if value is not None and hasattr(model_class, key):
                filtered_data[key] = value
        return model_class(**filtered_data)

    def dict(self) -> Dict[str, Any]:
        """
        Convert DTO to dictionary representation.
        """
        return asdict(self)

    def filtered_dict(
            self,
            exclude_none: bool = True,
            exclude_empty_str: bool = True
    ) -> Dict[str, Any]:
        """
        Convert the DTO to a dictionary and exclude certain 'empty' values.
        """
        raw_data = asdict(self)
        result = {}

        for key, value in raw_data.items():
            if exclude_none and value is None:
                continue
            if exclude_empty_str and value == "":
                continue
            result[key] = value

        return result
