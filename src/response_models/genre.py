import uuid
from typing import Optional

from models.common import CustomBaseModel


class GenreResponse(CustomBaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]


class GenreListResponse(CustomBaseModel):
    id: uuid.UUID
    name: str
