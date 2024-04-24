from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from src.models.user import User
from src.models.poll import PollInDB, PollWithVotes
from src.models.vote import Vote
from src.jwt import get_user_from_token
from src.polls import get_poll_in_db
from src.database import db

router = APIRouter()

async def update_vote(poll: PollInDB, username: str, old_option: int, new_option: int):
    if old_option == new_option:
        poll.options[old_option].votes -= 1
        await db.remove_vote(poll.id, username)
    else:
        poll.options[old_option].votes -= 1
        poll.options[new_option].votes += 1
        vote = Vote(poll_id=poll.id, username=username, option=new_option)
        await db.add_vote(vote)

@router.post("/api/polls/vote")
async def vote(token: Annotated[User, Depends(get_user_from_token)], poll: Annotated[PollInDB, Depends(get_poll_in_db)], option: int):
    if option < 0 or option >= len(poll.options):
        raise HTTPException(status_code=400, detail="Invalid option")
    
    old_option = await db.get_vote(poll.id, token.username)
    if old_option is not None:
        print("Updating vote")
        await update_vote(poll, token.username, old_option, option)
        poll_with_votes = PollWithVotes(title=poll.title, options=poll.options)
        await db.update_poll(poll.id, poll_with_votes)
    else:
        print("Adding vote")
        poll.options[option].votes += 1
        vote = Vote(poll_id=poll.id, username=token.username, option=option)
        await db.add_vote(vote)
        poll_with_votes = PollWithVotes(title=poll.title, options=poll.options)
        await db.update_poll(poll.id, poll_with_votes)
    
    return {"detail": "Vote added"}