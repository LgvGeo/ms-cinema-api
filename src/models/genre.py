import uuid
from typing import Optional

from common import CustomBaseModel


class Genre(CustomBaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
