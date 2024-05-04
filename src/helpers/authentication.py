from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from typing import Annotated

from src.services.sessions import sessions_service
from src.serializers.token import TokenSerializer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def authenticate_with_jwt(token: Annotated[str, Depends(oauth2_scheme)]) -> int | None:
    try:
        user_id = sessions_service.get_user_id(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Please log in")
    return user_id