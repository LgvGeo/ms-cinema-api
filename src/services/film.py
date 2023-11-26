import uuid
from functools import lru_cache

from fastapi import Depends

from db.abstract_cache_storage import CacheStorageInterface
from db.abstract_loaders import MovieLoaderInterface
from db.elastic_loaders import get_movie_loader
from db.redis_cache_storage import get_cache_storage
from models.service_models.film import Movie


class FilmService:
    def __init__(
            self, cache_storage: CacheStorageInterface,
            db: MovieLoaderInterface
    ):
        self.cache_storage = cache_storage
        self.db = db

    async def get_by_id(self, film_id: str) -> Movie | None:
        film = await self.cache_storage.get_from_cache(f'film:{film_id}')
        if film:
            return Movie.parse_raw(film)
        film = await self.db.get_film_by_id(film_id)
        if film:
            await self.cache_storage.put_to_cache(
                f'film:{film_id}', film.model_dump_json())
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


@lru_cache()
def get_film_service(
        cache_storage: CacheStorageInterface = Depends(get_cache_storage),
        db: MovieLoaderInterface = Depends(get_movie_loader),
) -> FilmService:
    return FilmService(cache_storage, db)
