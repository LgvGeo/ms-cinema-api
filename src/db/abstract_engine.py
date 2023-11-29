import uuid
from abc import ABC, abstractmethod
from typing import Any


class AsyncSearchEngine(ABC):
    @abstractmethod
    async def get_by_id(self, index: str, id: str) -> Any | None:
        pass

    @abstractmethod
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
        pass
