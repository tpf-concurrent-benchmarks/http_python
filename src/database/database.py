from src.models.user import UserInDB
from src.models.poll import Poll

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
    
    @abstractmethod
    async def add_poll(self, poll: Poll) -> int:
        pass

    @abstractmethod
    async def get_poll(self, poll_id: int) -> Poll | None:
        pass