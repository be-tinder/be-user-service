from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application._common.user_gateway import UserReader
from src.application._common.user_gateway import UserSaver
from src.application._common.user_gateway import UserUpdater
from src.domain.entities.user import UserDTO
from src.infrastructure.database.models.user import User


class UserDao(UserSaver, UserReader, UserUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save_user(self, data: UserDTO):
        data = data.filtered_dict(True, True)
        stmt = insert(User).values(**data).returning(User)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserDTO.from_orm(user) if user else None

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserDTO.from_orm(user) if user else None

    async def update_user(self, user_id: int, data: UserDTO):
        data = data.filtered_dict(True, True)
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data)
            .returning(User)
        )
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserDTO.from_orm(user) if user else None

    async def get_user_by_phone_number(self, phone_number: str) -> UserDTO:
        stmt = select(User).where(User.phone_number == phone_number)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserDTO.from_orm(user) if user else None
