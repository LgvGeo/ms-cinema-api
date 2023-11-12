import uuid

from models.common import CustomBaseModel


class GenreResponse(CustomBaseModel):
    id: uuid.UUID
    name: str
    description: str | None


class GenreListResponse(CustomBaseModel):
    id: uuid.UUID
    name: str
