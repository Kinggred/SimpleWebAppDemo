import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from SWADemo.api import auth
from SWADemo.api.auth import create_access_token, get_current_user
from SWADemo.config import settings
from SWADemo.crud.user import crud_users
from SWADemo.database import get_session
from SWADemo.models.auth import Token
from SWADemo.models.user import User, UserCreate, UserCreateModel, UserView

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_session),
) -> Token:
    user = crud_users.get_by_username(db, form_data.username)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id.__str__(), "username": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me", response_model=UserView)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.post("/users", response_model=UserView)
async def register_user(
    user: UserCreateModel,
    db: Session = Depends(get_session),
):
    user_model = UserCreate(username=user.username, hashed_password=auth.get_password_hash(user.password))
    return crud_users.create(db, user_model)
