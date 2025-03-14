from redis.asyncio import Redis


class RedisClient:
    def __init__(self, host: str, port: int, db: int) -> None:
        self._client = Redis(host=host, port=port, db=db)

    def get_client(self) -> Redis:
        return self._client
