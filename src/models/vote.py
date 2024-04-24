from pydantic import BaseModel

class Vote(BaseModel):
    username: str
    poll_id: int
    option: int