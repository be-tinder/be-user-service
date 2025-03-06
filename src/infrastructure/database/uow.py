from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interfaces.uow import IUoW


class UoW(IUoW):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
