from fastapi import APIRouter, HTTPException, Depends
from src.models.poll import Poll,PollInDB, PollWithVotes, Option
from src.database import db
from src.jwt import get_user_from_token
from src.models.user import User
from typing import Annotated, List

router = APIRouter()    

def create_poll_with_votes(poll: Poll) -> PollWithVotes:
    options = [Option(name=option, votes=0) for option in poll.options]
    return PollWithVotes(title=poll.title, options=options)

def transform_poll_in_db(poll: PollInDB) -> Poll:
    options = [option.name for option in poll.options]
    return Poll(title=poll.title, options=options)

async def get_poll_in_db(poll_id: int) -> PollInDB:
    poll = await db.get_poll(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

@router.get("/api/polls/{poll_id}", response_model=PollInDB)
async def get_poll(poll_id: int, token: Annotated[User, Depends(get_user_from_token)]) -> PollInDB:
    return await get_poll_in_db(poll_id)

@router.post("/api/polls", response_model=int)
async def create_poll(poll: Poll, token: Annotated[User, Depends(get_user_from_token)]) -> int:
    poll_with_votes = create_poll_with_votes(poll)
    poll_id = await db.add_poll(poll_with_votes)
    return poll_id

@router.get("/api/polls", response_model=List[Poll])
async def get_polls(token: Annotated[User, Depends(get_user_from_token)]) -> List[Poll]:
    polls = await db.get_polls()
    return [transform_poll_in_db(poll) for poll in polls]