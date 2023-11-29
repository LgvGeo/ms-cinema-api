import uuid
from functools import lru_cache

from fastapi import Depends

from db.abstract_cache_storage import CacheStorageInterface
from db.abstract_engine import AsyncSearchEngine
from db.elastic_engine import get_engine
from db.redis_cache_storage import get_cache_storage
from models.service_models.film import Movie
from services.abstract_service import BaseService


class FilmService(BaseService):
    def __init__(
            self, cache_storage: CacheStorageInterface,
            db: AsyncSearchEngine
    ):
        super().__init__(db, cache_storage, Movie)

    async def get_by_id(self, film_id: str) -> Movie | None:
        return await super().get_by_id(film_id, 'movies', 'film')

    async def get_films(
            self,
            page_size: int,
            page_number: int,
            sort: str | None = None,
            genre: uuid.UUID | None = None,
            title: str | None = None
    ) -> list[Movie]:
        return await super().get_multiple_elements(
            'movies',
            page_size,
            page_number,
            sort_field=sort,
            genre=genre,
            title=title
        )


@lru_cache()
def get_film_service(
        cache_storage: CacheStorageInterface = Depends(get_cache_storage),
        db: AsyncSearchEngine = Depends(get_engine),
) -> FilmService:
    return FilmService(cache_storage, db)
