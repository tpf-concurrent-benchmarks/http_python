from fastapi import APIRouter, HTTPException

from src.services.votes import votes_service
from src.helpers.dependencies import AuthDependency, DbDependency

router = APIRouter()

@router.post("/api/polls/{poll_id}/vote")
async def vote(poll_id: int, option: int, user_id: AuthDependency, db: DbDependency):
    try:
        votes_service.vote(db, poll_id, user_id, option)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))