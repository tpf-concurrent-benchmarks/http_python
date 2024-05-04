from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
import os

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

    @staticmethod
    def is_valid_timestamp(exp: int) -> bool:
        return datetime.fromtimestamp(exp, tz=timezone.utc) >= datetime.now(timezone.utc)
    
    def decode_jwt_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            return None
        if "exp" not in payload or not self.is_valid_timestamp(payload.get("exp")):
            return None
        return payload
    
jwt_manager = JWTManager()