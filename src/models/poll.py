from pydantic import BaseModel
from typing import List

class Option(BaseModel):
    name: str
    votes: int = 0

class PollWithVotes(BaseModel):
    title: str
    options: List[Option]

class PollInDB(PollWithVotes):
    id: int

class Poll(BaseModel):
    title: str
    options: List[str]

class PollGet(Poll):
    id: int