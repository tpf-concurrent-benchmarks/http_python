from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session


from src.services.sessions import sessions_service
from src.helpers.dependencies import DbDependency
from src.serializers.token import TokenSerializer

router = APIRouter()

UserPassForm = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/api/login", response_model=TokenSerializer)
async def login_for_token(form_data: UserPassForm,
                          db: DbDependency):
    token = sessions_service.create_token(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return token