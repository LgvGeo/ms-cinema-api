import uuid
from abc import ABC, abstractmethod

from models.service_models.film import Movie
from models.service_models.genre import Genre
from models.service_models.person import Person


class MovieLoaderInterface(ABC):
    @abstractmethod
    async def get_films(
            self,
            page_size: int,
            page_number: int,
            sort_field: str | None = None,
            genre: uuid.UUID | None = None,
            title: str | None = None
    ) -> list[Movie]:
        pass

    @abstractmethod
    async def get_film_by_id(self, film_id: str) -> Movie | None:
        pass


class GenreLoaderInterface(ABC):
    @abstractmethod
    async def get_genres(self) -> list[Genre]:
        pass

    @abstractmethod
    async def get_genre_by_id(self, genre_id: str) -> Genre | None:
        pass


class PersonLoaderInterface(ABC):
    @abstractmethod
    async def get_persons(
        self,
        page_size: int,
        page_number: int,
        name: str | None = None
    ) -> list[Person]:
        pass

    @abstractmethod
    async def get_person_by_id(self, person_id: str) -> Person | None:
        pass
