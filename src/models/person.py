import uuid

from models.common import CustomBaseModel


class MovieForPerson(CustomBaseModel):
    id: uuid.UUID
    title: str
    roles: list[str]


class Person(CustomBaseModel):
    id: uuid.UUID
    name: str
    films: list[MovieForPerson]
