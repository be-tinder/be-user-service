from typing import Optional

from src.domain.entities.user import UserDTO
from src.domain.interfaces.base_schema import BaseResponseSchema


class UserResponseSchema(BaseResponseSchema):
    data: Optional[UserDTO]


class AuthResponseSchema(BaseResponseSchema):
    data: Optional[dict]
