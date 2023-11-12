import uuid
from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.service_models.film import Movie

FILM_CACHE_EXPIRE_IN_SECONDS = 5 * 60


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Movie | None:
        film = await self._get_film_from_cache(film_id)
        if film:
            return film
        film = await self._get_film_from_elastic(film_id)
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
        films = await self._get_films_from_elastic(
            page_size, page_number,
            sort, genre, title
        )
        return films

    async def _get_films_from_elastic(
            self,
            page_size: int,
            page_number: int,
            sort_field: str | None = None,
            genre: uuid.UUID | None = None,
            title: str | None = None
    ) -> list[Movie] | None:
        filters = []
        body = {}
        sorts = []

        if sort_field:
            sort_order = 'asc'
            if sort_field.startswith('-'):
                sort_order = 'desc'
            sorts.append({
                 f'{sort_field.removeprefix("-")}': sort_order
            })
            body['sort'] = sorts

        if genre:
            filt = {
              'nested': {
                'path': 'genre',
                'query': {
                  'bool': {
                    'filter': [
                      {
                        'term': {'genre.id': f'{genre}'}
                      }
                    ]
                  }
                }
              }
            }
            filters.append(filt)

        if title:
            filt = {
                'match': {'title': f'{title}'}
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
            body=body, index='movies',
            from_=page_size*(page_number-1), size=page_size
        )
        return [Movie(**doc['_source']) for doc in result['hits']['hits']]

    async def _get_film_from_elastic(self, film_id: str) -> Movie | None:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Movie(**doc['_source'])

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
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
