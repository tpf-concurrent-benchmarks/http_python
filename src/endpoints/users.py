from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.hasher import hasher

from src.jwt import jwt_manager
from src.models.token import Token
from src.models.user import UserInDB
from src.database import db

router = APIRouter()

async def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = await db.get_user(username)
    if not user:
        return None
    if not hasher.verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(user: UserInDB) -> Token:
    access_token = jwt_manager.create_jwt_token({"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/api/login", response_model=Token)
async def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return create_access_token(user)


@router.post("/api/users", response_model=Token)
async def create_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    hashed_password = hasher.hash_password(form_data.password)
    user = UserInDB(username=form_data.username, hashed_password=hashed_password)
    new_user = await db.add_user(user)
    if not new_user:
        raise HTTPException(status_code=404, detail="Username already exists")
    return create_access_token(user)
