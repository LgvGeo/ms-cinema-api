import uuid

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.abstract_loaders import (GenreLoaderInterface, MovieLoaderInterface,
                                 PersonLoaderInterface)
from db.elastic import get_elastic
from models.service_models.film import Movie
from models.service_models.genre import Genre
from models.service_models.person import Person


class ElasticMovieLoader(MovieLoaderInterface):
    def __init__(self, connection):
        self.connection = connection

    async def get_films(
            self,
            page_size: int,
            page_number: int,
            sort_field: str | None = None,
            genre: uuid.UUID | None = None,
            title: str | None = None
    ) -> list[Movie]:
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

        result = await self.connection.search(
            body=body, index='movies',
            from_=page_size*(page_number-1), size=page_size
        )
        return [Movie(**doc['_source']) for doc in result['hits']['hits']]

    async def get_film_by_id(self, film_id: str) -> Movie | None:
        try:
            doc = await self.connection.get(index='movies', id=film_id)
        except NotFoundError:
            return None
        return Movie(**doc['_source'])


class ElasticGenreLoader(GenreLoaderInterface):
    def __init__(self, connection):
        self.connection = connection

    async def get_genres(self) -> list[Genre]:
        result = await self.connection.search(
            index='genres',
            from_=0, size=10000
        )
        return [Genre(**doc['_source']) for doc in result['hits']['hits']]

    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        try:
            doc = await self.connection.get(index='genres', id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])


class ElasticPersonLoader(PersonLoaderInterface):
    def __init__(self, connection):
        self.connection = connection

    async def get_persons(
        self,
        page_size: int,
        page_number: int,
        name: str | None = None
    ) -> list[Person]:
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

        result = await self.connection.search(
            body=body, index='persons',
            from_=page_size*(page_number-1), size=page_size
        )
        return [Person(**doc['_source']) for doc in result['hits']['hits']]

    async def get_person_by_id(self, person_id: str) -> Person | None:
        try:
            doc = await self.connection.get(index='persons', id=person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])


async def get_movie_loader(
        elastic: AsyncElasticsearch = Depends(get_elastic)
):
    return ElasticMovieLoader(elastic)


async def get_genre_loader(
        elastic: AsyncElasticsearch = Depends(get_elastic)
):
    return ElasticGenreLoader(elastic)


async def get_person_loader(
        elastic: AsyncElasticsearch = Depends(get_elastic)
):
    return ElasticPersonLoader(elastic)
