from functools import lru_cache

from fastapi import Depends

from db.abstract_cache_storage import CacheStorageInterface
from db.abstract_loaders import PersonLoaderInterface
from db.elastic_loaders import get_person_loader
from db.redis_cache_storage import get_cache_storage
from models.service_models.person import Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 5 * 60


class PersonService:
    def __init__(
            self,
            cache_storage: CacheStorageInterface,
            db: PersonLoaderInterface
    ):
        self.cache_storage = cache_storage
        self.db = db

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self.cache_storage.get_from_cache(f'person:{person_id}')
        if person:
            return Person.parse_raw(person)
        person = await self.db.get_person_by_id(person_id)
        if person:
            await self.cache_storage.put_to_cache(
                f'person:{person_id}', person.model_dump_json())
        return person

    async def get_persons(
            self,
            page_size: int,
            page_number: int,
            name: str | None = None
    ) -> list[Person]:
        persons = await self.db.get_persons(
            page_size, page_number,
            name
        )
        return persons


@lru_cache()
def get_person_service(
        cache_storage: CacheStorageInterface = Depends(get_cache_storage),
        db: PersonLoaderInterface = Depends(get_person_loader),
) -> PersonService:
    return PersonService(cache_storage, db)
