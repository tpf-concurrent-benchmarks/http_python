from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from typing import Annotated

from src.models.user import User

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

class JWTManager:
    def __init__(self):
        self.secret_key = os.environ["SECRET_KEY"]
        self.access_token_expire_minutes = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
        self.algorithm = os.environ["ALGORITHM"]

    def create_jwt_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_jwt_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
jwt_manager = JWTManager()

def get_user_from_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    payload = jwt_manager.decode_jwt_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(username=payload.get("sub"))