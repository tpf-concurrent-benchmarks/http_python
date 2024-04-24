from src.models.user import UserInDB
from src.models.poll import PollInDB, PollWithVotes
from src.models.vote import Vote
from typing import List

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
    async def add_poll(self, poll: PollWithVotes) -> int:
        pass

    @abstractmethod
    async def update_poll(self, poll_id: int, poll: PollWithVotes) -> bool:
        pass

    @abstractmethod
    async def get_poll(self, poll_id: int) -> PollInDB | None:
        pass

    @abstractmethod
    async def get_polls(self) -> List[PollInDB]:
        pass

    @abstractmethod
    async def add_vote(self, poll_id: int, username: str, option: int) -> bool:
        pass

    @abstractmethod
    async def get_vote(self, poll_id: int, username: str) -> int | None:
        pass

    @abstractmethod
    async def remove_vote(self, poll_id: int, username: str) -> bool:
        pass