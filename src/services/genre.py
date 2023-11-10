from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 5 * 60


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_genre_from_cache(genre_id)
        if genre:
            return genre
        genre = await self._get_genre_from_elastic(genre_id)
        if genre:
            await self._put_genre_to_cache(genre)
        return genre

    async def get_genres(self) -> list[Genre]:
        genres = await self._get_genres_from_elastic()
        return genres

    async def _get_genres_from_elastic(self):
        result = await self.elastic.search(
            index='genres',
            from_=0, size=10000
        )
        return [Genre(**doc['_source']) for doc in result['hits']['hits']]

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        try:
            doc = await self.elastic.get(index='genres', id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])

    async def _get_genre_from_cache(self, genre_id: str) -> Optional[Genre]:
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
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
