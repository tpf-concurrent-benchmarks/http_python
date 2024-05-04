from pydantic import BaseModel

class PollPreviewSerializer(BaseModel):
    poll_id: int
    poll_topic: str

    class Config:
        orm_mode = True