import uuid

from elasticsearch import NotFoundError
from fastapi import Depends

from db.abstract_engine import AsyncSearchEngine
from db.elastic import get_elastic


class ElasticAsyncSearchEngine(AsyncSearchEngine):

    def __init__(self, connection):
        self.connection = connection

    async def get_by_id(self, index: str, id: str) -> dict | None:
        try:
            doc = await self.connection.get(index=index, id=id)
        except NotFoundError:
            return None
        return doc['_source']

    async def get_multuple_elements(
        self,
        index: str,
        page_size: int,
        page_number: int,
        name: str | None = None,
        sort_field: str | None = None,
        genre: uuid.UUID | None = None,
        title: str | None = None
    ) -> list[dict]:
        filters = []
        body = {}
        sorts = []

        if name:
            filt = {
                'match': {'name': f'{name}'}
            }
            filters.append(filt)

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
            body=body, index=index,
            from_=page_size*(page_number-1), size=page_size
        )
        return [doc['_source'] for doc in result['hits']['hits']]


def get_engine(connection=Depends(get_elastic)):
    return ElasticAsyncSearchEngine(connection)
