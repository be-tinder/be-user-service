from typing import Any

from redis.asyncio import Redis

from src.domain.interfaces.redis import RedisGateway


class RedisManager(RedisGateway):
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get(self, key: str) -> Any:
        return await self.redis_client.get(key)

    async def set(self, key: str, value: Any, expire: int = None) -> None:
        await self.redis_client.set(key, value)
        if expire:
            await self.redis_client.expire(key, expire)
