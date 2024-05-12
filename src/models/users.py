from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List

from src.helpers.hasher import hasher
from src.models import Base

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    hashed_password = Column(String(128))
    
    @staticmethod
    async def find(db: AsyncSession, user_id: int) -> Optional["UserModel"]:
        return await db.get(UserModel, user_id)
    
    @staticmethod
    async def find_by_username(db: AsyncSession, username: str) -> Optional["UserModel"]:
        iter = (await db.execute(select(UserModel).filter(UserModel.username == username))).unique()
        try:
            user = next(iter)
            return user[0]
        except StopIteration:
            return None
    
    @staticmethod
    async def create(db: AsyncSession, username: str, password: str) -> "UserModel":
        user = UserModel(username=username, hashed_password=hasher.hash_password(password))
        db.add(user)
        await db.flush()
        return user

    def authenticate(self, password: str) -> bool:
        return hasher.verify_password(password, self.hashed_password)
    
    @staticmethod
    async def get_all(db: AsyncSession) -> List["UserModel"]:
        return await db.execute(select(UserModel))