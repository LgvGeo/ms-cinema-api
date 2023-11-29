from functools import lru_cache

from fastapi import Depends

from db.abstract_cache_storage import CacheStorageInterface
from db.abstract_engine import AsyncSearchEngine
from db.elastic_engine import get_engine
from db.redis_cache_storage import get_cache_storage
from models.service_models.genre import Genre
from services.abstract_service import BaseService


class GenreService(BaseService):
    def __init__(
            self, cache_storage: CacheStorageInterface,
            db: AsyncSearchEngine
    ):
        super().__init__(db, cache_storage, Genre)

    async def get_by_id(self, genre_id: str) -> Genre | None:
        return await super().get_by_id(genre_id, 'genres', 'genre')

    async def get_genres(self) -> list[Genre]:
        return await super().get_multiple_elements('genres', 1000, 1)


@lru_cache()
def get_genre_service(
        cache_storage: CacheStorageInterface = Depends(get_cache_storage),
        db: AsyncSearchEngine = Depends(get_engine),
) -> GenreService:
    return GenreService(cache_storage, db)
