from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person

PERSON_CACHE_EXPIRE_IN_SECONDS = 5 * 60


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[Person]:
        person = await self._get_peson_from_cache(person_id)
        if person:
            return person
        person = await self._get_person_from_elastic(person_id)
        await self._put_person_to_cache(person)
        return person

    async def get_persons(
            self,
            page_size: int,
            page_number: int,
            name: str | None = None
    ) -> list[Person]:
        persons = await self._get_persons_from_elastic(
            page_size, page_number,
            name
        )
        return persons

    async def _get_persons_from_elastic(
            self,
            page_size: int,
            page_number: int,
            name: str | None = None
    ) -> Optional[list[Person]]:
        filters = []
        body = {}

        if name:
            filt = {
                'match': {'name': f'{name}'}
            }
            filters.append(filt)
        if filters:
            query = {
                 'bool': {
                      'filter': filters
                    }
            }
            body['query'] = query

        result = await self.elastic.search(
            body=body, index='persons',
            from_=page_size*(page_number-1), size=page_size
        )
        return [Person(**doc['_source']) for doc in result['hits']['hits']]

    async def _get_person_from_elastic(
            self, person_id: str
    ) -> Optional[Person]:
        try:
            doc = await self.elastic.get(index='persons', id=person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])

    async def _get_peson_from_cache(self, person_id: str) -> Optional[Person]:
        key = f'person:{person_id}'
        data = await self.redis.get(key)
        if not data:
            return None
        return Person.parse_raw(data)

    async def _put_person_to_cache(self, genre: Person):
        key = f'person:{genre.id}'
        await self.redis.set(
            key, genre.model_dump_json(),
            PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
