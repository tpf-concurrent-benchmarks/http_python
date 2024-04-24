from fastapi import APIRouter, HTTPException, Depends
from src.models.poll import Poll
from src.database import db
from src.jwt import get_user_from_token
from src.models.user import User
from typing import Annotated

router = APIRouter()

@router.get("/api/polls/{poll_id}", response_model=Poll)
async def get_poll(poll_id: int, token: Annotated[User, Depends(get_user_from_token)]) -> Poll:
    poll = await db.get_poll(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

@router.post("/api/polls", response_model=int)
async def create_poll(poll: Poll, token: Annotated[User, Depends(get_user_from_token)]) -> int:
    poll_id = await db.add_poll(poll)
    return poll_id