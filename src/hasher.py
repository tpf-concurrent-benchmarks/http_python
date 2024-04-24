from dotenv import load_dotenv
import os
from passlib.context import CryptContext

load_dotenv()

class Hasher:
    def __init__(self):
        self.secret_key = os.environ["SECRET_KEY"]
        self.algorithm = os.environ["ALGORITHM"]
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

hasher = Hasher()