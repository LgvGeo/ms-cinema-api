import uuid

from models.common import CustomBaseModel


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
    description: str | None
    director: list[str]
    genre: list[GenreForMovie]
    imdb_rating: float | None
    title: str
    writers: list[PersonForMovie]
    writers_names: list[str]
