from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from SWADemo.api.auth import get_current_user
from SWADemo.crud.file import crud_files
from SWADemo.crud.user import crud_users
from SWADemo.database import get_session
from SWADemo.models.file import FileView
from SWADemo.models.user import User

router = APIRouter()

router.get("", response_model=FileView)
def get_user_files(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_session())):
    return crud_users.get_user_files(db, current_user)


router.post("")
def upload_file(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_session())):
    pass
