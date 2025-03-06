from typing import List, Optional, Dict

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import UserDTO
from src.domain.repositories.iuser_repository import IUserRepository
from src.infrastructure.database.models.user import User


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, data: UserDTO) -> UserDTO:
        stmt = insert(User).values(**data.dict()).returning(User)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserDTO.from_orm(user) if user else None

    async def get_by_id(self, user_id: int) -> Optional[UserDTO]:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserDTO.from_orm(user) if user else None

    async def update(self, user_id: int, data: UserDTO) -> Optional[UserDTO]:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(**data.dict())
            .returning(User)
        )
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserDTO.from_orm(user) if user else None

    async def remove(self, user_id: int) -> bool:
        stmt = delete(User).where(User.id == user_id)
        await self._session.execute(stmt)
        return stmt.is_delete

    async def list(self, filters: Optional[Dict] = None) -> List[UserDTO]:
        stmt = select(User)
        if filters:
            stmt = stmt.filter_by(**filters)

        result = await self._session.execute(stmt)
        users = result.scalars().all()
        return [UserDTO.from_orm(user) for user in users]
