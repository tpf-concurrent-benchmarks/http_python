from fastapi import APIRouter, HTTPException
from typing import List

from src.services.polls import polls_service
from src.helpers.dependencies import AuthDependency, DbDependency
from src.serializers.polls.full_poll import FullPollSerializer
from src.serializers.polls.poll_creation import PollCreationSerializer
from src.serializers.polls.poll_creation_output import PollCreationOutputSerializer
from src.serializers.polls.all_polls import AllPollsSerializer

router = APIRouter()    

@router.get("/api/polls/{poll_id}", response_model=FullPollSerializer)
async def get_poll(poll_id: int, db: DbDependency):
    poll = polls_service.get(db, poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll

@router.post("/api/polls", response_model=PollCreationOutputSerializer)
async def create_poll(poll_in: PollCreationSerializer, user_id: AuthDependency, db: DbDependency):
    try:
        poll = polls_service.create(db, user_id, poll_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return poll

@router.get("/api/polls", response_model=AllPollsSerializer)
async def get_polls(db: DbDependency):
    return polls_service.get_all(db)
    
@router.delete("/api/polls/{poll_id}")
async def delete_poll(poll_id: int, user_id: AuthDependency, db: DbDependency):
    try:
        polls_service.delete(db, poll_id, user_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    return {"detail": "Poll deleted"}