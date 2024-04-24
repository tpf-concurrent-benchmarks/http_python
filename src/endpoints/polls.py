from fastapi import APIRouter, Depends
from src.models.poll import Poll,PollInDB, PollWithVotes, Option
from src.database import db
from src.jwt import get_user_from_token
from src.models.user import User
from typing import Annotated, List
from src import utils

router = APIRouter()    

def create_poll_with_votes(poll: Poll) -> PollWithVotes:
    options = [Option(name=option, votes=0) for option in poll.options]
    return PollWithVotes(title=poll.title, options=options)

def transform_poll_in_db(poll: PollInDB) -> Poll:
    options = [option.name for option in poll.options]
    return Poll(title=poll.title, options=options)

@router.get("/api/polls/{poll_id}", response_model=PollInDB)
async def get_poll(poll: Annotated[PollInDB, Depends(utils.get_poll_in_db)], token: Annotated[User, Depends(get_user_from_token)]) -> PollInDB:
    return poll

@router.post("/api/polls", response_model=int)
async def create_poll(poll: Poll, token: Annotated[User, Depends(get_user_from_token)]) -> int:
    poll_with_votes = create_poll_with_votes(poll)
    poll_id = await db.add_poll(poll_with_votes)
    return poll_id

@router.get("/api/polls", response_model=List[Poll])
async def get_polls(token: Annotated[User, Depends(get_user_from_token)]) -> List[Poll]:
    polls = await db.get_polls()
    return [transform_poll_in_db(poll) for poll in polls]