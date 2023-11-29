import abc
import json
import uuid

from pydantic import BaseModel

from db.abstract_cache_storage import CacheStorageInterface
from db.abstract_engine import AsyncSearchEngine


class BaseService(abc.ABC):
    def __init__(
            self,
            search_engine: AsyncSearchEngine,
            cache_storage: CacheStorageInterface,
            model: BaseModel
    ):
        self.search_engine = search_engine
        self.cache_storage = cache_storage
        self.model = model

    async def get_by_id(
            self,
            id: str,
            index,
            cache_prefix
    ) -> BaseModel | None:
        obj = await self.cache_storage.get_from_cache(f'{cache_prefix}:{id}')
        if obj:
            return self.model.parse_raw(obj)
        obj = await self.search_engine.get_by_id(index, id)
        if obj:
            await self.cache_storage.put_to_cache(
                f'{cache_prefix}:{id}', json.dumps(obj))
            return self.model(**obj)
        return obj

    async def get_multiple_elements(
        self,
        index: str,
        page_size: int,
        page_number: int,
        name: str | None = None,
        sort_field: str | None = None,
        genre: uuid.UUID | None = None,
        title: str | None = None
    ) -> list[BaseModel]:
        res = await self.search_engine.get_multuple_elements(
            index,
            page_size,
            page_number,
            name=name,
            sort_field=sort_field,
            genre=genre,
            title=title
        )
        return [self.model(**x) for x in res]
