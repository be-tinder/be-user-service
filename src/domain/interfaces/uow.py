from abc import ABC


class IUoW(ABC):
    async def commit(self):
        pass

    async def rollback(self):
        pass
