from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from typing import Optional

from src.helpers.hasher import hasher
from src.models import Base

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    @staticmethod
    def find(db: Session, user_id: int) -> Optional["UserModel"]:
        return db.query(UserModel).filter(UserModel.user_id == user_id).first()
    
    @staticmethod
    def find_by_username(db: Session, username: str) -> Optional["UserModel"]:
        return db.query(UserModel).filter(UserModel.username == username).first()
    
    @staticmethod
    def create(db: Session, username: str, password: str) -> "UserModel":
        user = UserModel(username=username, hashed_password=hasher.hash_password(password))
        db.add(user)
        db.flush()
        return user

    def authenticate(self, password: str) -> bool:
        return hasher.verify_password(password, self.hashed_password)