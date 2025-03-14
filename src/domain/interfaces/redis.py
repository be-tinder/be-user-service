from typing import Protocol, Any


class RedisGateway(Protocol):
    async def get(self, key: str) -> Any:
        pass

    async def set(self, key: str, value: Any, expire: int = None) -> None:
        pass
