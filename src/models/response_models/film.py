import uuid

from models.common import CustomBaseModel


class PersonForMovie(CustomBaseModel):
    id: uuid.UUID
    name: str


class GenreForMovie(CustomBaseModel):
    id: uuid.UUID
    name: str


class MovieResponse(CustomBaseModel):
    id: uuid.UUID
    actors: list[PersonForMovie]
    description: str | None
    director: list[str]
    genre: list[GenreForMovie]
    imdb_rating: float | None
    title: str
    writers: list[PersonForMovie]


class MoviesListResponse(CustomBaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float | None
