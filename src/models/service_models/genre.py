import uuid

from models.common import CustomBaseModel


class Genre(CustomBaseModel):
    id: uuid.UUID
    name: str
    description: str | None
