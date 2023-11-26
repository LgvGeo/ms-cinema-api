from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from db.abstract_loaders import GenreLoaderInterface
from db.elastic_loaders import get_genre_loader
from db.redis import get_redis
from models.service_models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 5 * 60


class GenreService:
    def __init__(self, redis: Redis, db: GenreLoaderInterface):
        self.redis = redis
        self.db = db

    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre = await self._get_genre_from_cache(genre_id)
        if genre:
            return genre
        genre = await self.db.get_genre_by_id(genre_id)
        if genre:
            await self._put_genre_to_cache(genre)
        return genre

    async def get_genres(self) -> list[Genre]:
        genres = await self.db.get_genres()
        return genres

    async def _get_genre_from_cache(self, genre_id: str) -> Genre | None:
        key = f'genre:{genre_id}'
        data = await self.redis.get(key)
        if not data:
            return None
        return Genre.parse_raw(data)

    async def _put_genre_to_cache(self, genre: Genre):
        key = f'genre:{genre.id}'
        await self.redis.set(
            key, genre.model_dump_json(),
            GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        db: GenreLoaderInterface = Depends(get_genre_loader),
) -> GenreService:
    return GenreService(redis, db)
