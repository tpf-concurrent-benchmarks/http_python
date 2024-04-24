from src.models.poll import Poll
from src.models.user import UserInDB
from src.database.database import DataBase
from typing import List

class InMemoryDataBase(DataBase):
    def __init__(self):
        self.users = {}
        self.polls = {}
        self.next_poll_id = 1

    async def get_user(self, username: str) -> UserInDB | None:
        if username in self.users:
            user_dict = self.users[username]
            return UserInDB(**user_dict)
        return None
    
    async def add_user(self, user: UserInDB) -> bool:
        if user.username in self.users:
            return False
        self.users[user.username] = user.dict()
        return True
    
    async def add_poll(self, poll: Poll) -> int:
        poll_id = self.next_poll_id
        self.polls[poll_id] = poll.dict()
        self.next_poll_id += 1
        return poll_id
    
    async def get_poll(self, poll_id: int) -> Poll | None:
        if poll_id in self.polls:
            poll_dict = self.polls[poll_id]
            return Poll(**poll_dict)
        return None
    