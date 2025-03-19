import uuid
from uuid import UUID

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: UUID = Field(primary_key=True, default=uuid.uuid4())
