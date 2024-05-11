from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from typing import Annotated

from src.services.sessions import sessions_service

security = HTTPBearer()

def authenticate_with_jwt(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> int | None:
    try:
        user_id = sessions_service.get_user_id(credentials.credentials)
    except ValueError:
        raise HTTPException(status_code=401, detail="Please log in")
    return user_id