from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from src.services.users import users_service
from src.services.sessions import sessions_service
from src.database import get_db
from src.serializers.token import TokenSerializer
from src.serializers.users.user_creation import UserCreationSerializer
from src.models.users import UserModel

router = APIRouter()


@router.post("/api/users", response_model=TokenSerializer)
async def create_user(user_serializer: UserCreationSerializer,
                      db: Session = Depends(get_db)):
    user = await users_service.create_user(db, user_serializer)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return sessions_service.create_token_for(user.user_id)

@router.get("/api/users")
async def get_users(db: Session = Depends(get_db)):
    return await UserModel.get_all(db)