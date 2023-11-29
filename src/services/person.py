from functools import lru_cache

from fastapi import Depends

from db.abstract_cache_storage import CacheStorageInterface
from db.abstract_engine import AsyncSearchEngine
from db.elastic_engine import get_engine
from db.redis_cache_storage import get_cache_storage
from models.service_models.person import Person
from services.abstract_service import BaseService


class PersonService(BaseService):
    def __init__(
            self, cache_storage: CacheStorageInterface,
            db: AsyncSearchEngine
    ):
        super().__init__(db, cache_storage, Person)

    async def get_by_id(self, person_id: str) -> Person | None:
        return await super().get_by_id(person_id, 'persons', 'person')

    async def get_persons(
            self,
            page_size: int,
            page_number: int,
            name: str | None = None
    ) -> list[Person]:
        return await super().get_multiple_elements(
            'persons', page_size, page_number, name=name)


@lru_cache()
def get_person_service(
        cache_storage: CacheStorageInterface = Depends(get_cache_storage),
        db: AsyncSearchEngine = Depends(get_engine),
) -> PersonService:
    return PersonService(cache_storage, db)
