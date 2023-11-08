import uuid
from typing import Optional

from models.common import CustomBaseModel


class Genre(CustomBaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
