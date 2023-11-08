import uuid
from typing import Optional

from common import CustomBaseModel


class PersonForMovie(CustomBaseModel):
    id: uuid.UUID
    name: str


class GenreForMovie(CustomBaseModel):
    id: uuid.UUID
    name: str


class Movie(CustomBaseModel):
    id: uuid.UUID
    actors: list[PersonForMovie]
    actors_names: list[str]
    description: Optional[str]
    director: list[str]
    genre: list[GenreForMovie]
    imdb_rating: Optional[float]
    title: str
    writers: list[PersonForMovie]
    writers_names: list[str]
