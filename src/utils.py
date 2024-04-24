from fastapi import HTTPException
from src.database import db
from src.models.poll import PollInDB

async def get_poll_in_db(poll_id: int) -> PollInDB | None:
    poll = await db.get_poll(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    return poll