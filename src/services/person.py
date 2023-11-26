from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from db.abstract_loaders import PersonLoaderInterface
from db.elastic_loaders import get_person_loader
from db.redis import get_redis
from models.service_models.person import Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 5 * 60


class PersonService:
    def __init__(self, redis: Redis, db: PersonLoaderInterface):
        self.redis = redis
        self.db = db

    async def get_by_id(self, person_id: str) -> Person | None:
        person = await self._get_peson_from_cache(person_id)
        if person:
            return person
        person = await self.db.get_person_by_id(person_id)
        if person:
            await self._put_person_to_cache(person)
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

    async def _get_peson_from_cache(self, person_id: str) -> Person | None:
        key = f'person:{person_id}'
        data = await self.redis.get(key)
        if not data:
            return None
        return Person.parse_raw(data)

    async def _put_person_to_cache(self, person: Person):
        key = f'person:{person.id}'
        await self.redis.set(
            key, person.model_dump_json(),
            PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        db: PersonLoaderInterface = Depends(get_person_loader),
) -> PersonService:
    return PersonService(redis, db)
