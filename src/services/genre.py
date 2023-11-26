from functools import lru_cache

from fastapi import Depends

from db.abstract_cache_storage import CacheStorageInterface
from db.abstract_loaders import GenreLoaderInterface
from db.elastic_loaders import get_genre_loader
from db.redis_cache_storage import get_cache_storage
from models.service_models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 5 * 60


class GenreService:
    def __init__(
            self,
            cache_storage: CacheStorageInterface,
            db: GenreLoaderInterface
    ):
        self.cache_storage = cache_storage
        self.db = db

    async def get_by_id(self, genre_id: str) -> Genre | None:
        genre = await self.cache_storage.get_from_cache(f'genre:{genre_id}')
        if genre:
            return Genre.parse_raw(genre)
        genre = await self.db.get_genre_by_id(genre_id)
        if genre:
            await self.cache_storage.put_to_cache(
                f'genre:{genre_id}', genre.model_dump_json())
        return genre

    async def get_genres(self) -> list[Genre]:
        genres = await self.db.get_genres()
        return genres


@lru_cache()
def get_genre_service(
        cache_storage: CacheStorageInterface = Depends(get_cache_storage),
        db: GenreLoaderInterface = Depends(get_genre_loader),
) -> GenreService:
    return GenreService(cache_storage, db)
