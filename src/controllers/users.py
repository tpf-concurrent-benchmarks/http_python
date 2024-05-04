from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from src.services.users import users_service
from src.services.sessions import sessions_service
from src.database import get_db
from src.serializers.token import TokenSerializer

router = APIRouter()

UserPassForm = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/api/users", response_model=TokenSerializer)
def create_user(form_data: UserPassForm,
                      db: Session = Depends(get_db)):
    user = users_service.create_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return sessions_service.create_token_for(user.user_id)