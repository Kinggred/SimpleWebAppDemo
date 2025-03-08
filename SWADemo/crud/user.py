from fastapi import HTTPException
from sqlmodel import Session, select

from SWADemo.crud.base import CRUDBase
from SWADemo.models.user import User, UserCreate


class CRUDUser(CRUDBase[User, UserCreate]):
    @staticmethod
    def get_by_username(db: Session, username: str) -> User:
        user = db.exec(select(User).where(User.username == username)).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


crud_users = CRUDUser(User)
