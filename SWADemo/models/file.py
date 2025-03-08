from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel

from SWADemo.models.base import BaseModel


class File(BaseModel, table=True):
    name: str | None
    key: str
    uploaded_by: UUID = Field(default_factory=uuid4, foreign_key="user.id")

class FileView(SQLModel):
    name: str | None
    id: UUID