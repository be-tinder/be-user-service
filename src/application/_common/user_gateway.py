from typing import Protocol

from src.domain.entities.user import UserDTO


class UserReader(Protocol):
    async def get_user_by_id(self, user_id: int) -> UserDTO:
        raise NotImplementedError

    async def get_user_by_phone_number(self, phone_number: str) -> UserDTO:
        raise NotImplementedError


class UserSaver(Protocol):
    async def save_user(self, user: UserDTO) -> None:
        raise NotImplementedError


class UserUpdater(Protocol):
    async def update_user(self, user_id: int, user: UserDTO) -> None:
        raise NotImplementedError