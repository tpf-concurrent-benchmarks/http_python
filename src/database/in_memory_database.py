from src.models.poll import PollInDB, Poll, PollWithVotes
from src.models.user import UserInDB
from src.database.database import DataBase
from src.models.vote import Vote
from typing import List

class InMemoryDataBase(DataBase):
    def __init__(self):
        self.users = {}
        self.polls = {}
        self.votes = {}
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
    
    async def add_poll(self, poll: PollWithVotes) -> int:
        poll_id = self.next_poll_id
        self.polls[poll_id] = poll.dict()
        self.next_poll_id += 1
        return poll_id
    
    async def update_poll(self, poll_id: int, poll: PollWithVotes) -> bool:
        if poll_id in self.polls:
            self.polls[poll_id] = poll.dict()
            return True
        return False
    
    async def get_poll(self, poll_id: int) -> PollInDB | None:
        if poll_id in self.polls:
            poll_dict = self.polls[poll_id]
            return PollInDB(id=poll_id, **poll_dict)
        return None
    
    async def get_polls(self) -> List[PollInDB]:
        polls = []
        for poll_id, poll_dict in self.polls.items():
            poll = PollInDB(id=poll_id, **poll_dict)
            polls.append(poll)
        return polls
    
    async def add_vote(self, poll_id: int, username: str, option: int) -> bool:
        self.votes[(poll_id, username)] = option
        return True
    
    async def get_vote(self, poll_id: int, username: str) -> int | None:
        return self.votes.get((poll_id, username), None)
    
    async def remove_vote(self, poll_id: int, username: str) -> bool:
        if (poll_id, username) in self.votes:
            del self.votes[(poll_id, username)]
            return True
        return False