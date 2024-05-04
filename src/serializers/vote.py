from pydantic import BaseModel

class VoteSerializer(BaseModel):
    user_id: str
    poll_id: int
    option: int