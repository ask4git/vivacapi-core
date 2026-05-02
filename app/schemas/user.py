import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: uuid.UUID
    email: str
    name: str | None
    picture: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
