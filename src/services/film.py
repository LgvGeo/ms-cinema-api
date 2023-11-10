import uuid
from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.film import Movie


class FilmService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Movie]:
        film = await self._get_film_from_elastic(film_id)
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
    ) -> Optional[list[Movie]]:
        filters = []
        body = {}
        sorts = []

        if sort_field:
            sort_order = 'asc'
            if sort_field.startswith('-'):
                sort_order = 'desc'
            sorts.append({
                 f"{sort_field.removeprefix('-')}": sort_order
            })
            body['sort'] = sorts

        if genre:
            filt = {
              "nested": {
                "path": "genre",
                "query": {
                  "bool": {
                    "filter": [
                      {
                        "term": {"genre.id": f"{genre}"}
                      }
                    ]
                  }
                }
              }
            }
            filters.append(filt)

        if title:
            filt = {
                "match": {"title": f"{title}"}
            }
            filters.append(filt)
        if filters:
            query = {
                 "bool": {
                      "filter": filters
                    }
            }
            body["query"] = query

        result = await self.elastic.search(
            body=body, index='movies',
            from_=page_size*(page_number-1), size=page_size
        )
        return [Movie(**doc['_source']) for doc in result['hits']['hits']]

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Movie]:
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Movie(**doc['_source'])


@lru_cache()
def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic)
