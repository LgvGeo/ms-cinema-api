from fastapi import Depends

from db.abstract_cache_storage import CacheStorageInterface
from db.redis import get_redis

CACHE_EXPIRE_IN_SECONDS = 5 * 60


class RedisCacheStorage(CacheStorageInterface):
    def __init__(self, connection):
        self.connection = connection

    async def get_from_cache(self, key: str) -> str | None:
        data = await self.connection.get(key)
        if not data:
            return None
        return data

    async def put_to_cache(self, key: str, value: str) -> None:
        await self.connection.set(
            key, value,
            CACHE_EXPIRE_IN_SECONDS)


def get_cache_storage(connection=Depends(get_redis)):
    return RedisCacheStorage(connection)
