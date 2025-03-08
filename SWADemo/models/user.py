from sqlmodel import SQLModel

from SWADemo.models.base import BaseModel


class UserCreateModel(SQLModel):
    username: str
    password: str


class UserCreate(SQLModel):
    username: str
    hashed_password: str


class UserView(BaseModel):
    username: str


class User(BaseModel, UserCreate, table=True):
    pass
