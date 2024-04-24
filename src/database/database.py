from src.models.user import UserInDB
from abc import ABC, abstractmethod


class DataBase(ABC):
    def __init__(self):
        self.users = {}

    @abstractmethod
    async def get_user(self, username: str) -> UserInDB | None:
        pass
    
    @abstractmethod
    async def add_user(self, user: UserInDB) -> bool:
        pass
    