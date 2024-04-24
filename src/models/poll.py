from pydantic import BaseModel
from typing import List

class Option(BaseModel):
    name: str
    votes: int = 0

class PollInDB(BaseModel):
    id: int
    title: str
    options: List[Option]

class PollWithVotes(BaseModel):
    title: str
    options: List[Option]

class Poll(BaseModel):
    title: str
    options: List[str]