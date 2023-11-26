from abc import ABC, abstractmethod


class CacheStorageInterface(ABC):
    @abstractmethod
    def get_from_cache(self, key: str) -> str | None:
        pass

    @abstractmethod
    def put_to_cache(sekf, key: str, value: str) -> None:
        pass
