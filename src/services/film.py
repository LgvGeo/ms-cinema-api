import uuid
from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from db.abstract_loaders import MovieLoaderInterface
from db.elastic_loaders import get_movie_loader
from db.redis import get_redis
from models.service_models.film import Movie

FILM_CACHE_EXPIRE_IN_SECONDS = 5 * 60


class FilmService:
    def __init__(self, redis: Redis, db: MovieLoaderInterface):
        self.redis = redis
        self.db = db

    async def get_by_id(self, film_id: str) -> Movie | None:
        film = await self._get_film_from_cache(film_id)
        if film:
            return film
        film = await self.db.get_film_by_id(film_id)
        if film:
            await self._put_film_to_cache(film)
        return film

    async def get_films(
            self,
            page_size: int,
            page_number: int,
            sort: str | None = None,
            genre: uuid.UUID | None = None,
            title: str | None = None
    ) -> list[Movie]:
        films = await self.db.get_films(
            page_size, page_number,
            sort, genre, title
        )
        return films

    async def _get_film_from_cache(self, film_id: str) -> Movie | None:
        key = f'film:{film_id}'
        data = await self.redis.get(key)
        if not data:
            return None
        return Movie.parse_raw(data)

    async def _put_film_to_cache(self, film: Movie):
        key = f'film:{film.id}'
        await self.redis.set(
            key, film.model_dump_json(),
            FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        db: MovieLoaderInterface = Depends(get_movie_loader),
) -> FilmService:
    return FilmService(redis, db)
