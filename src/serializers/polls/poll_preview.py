from pydantic import BaseModel
from src.models.polls import PollModel

class PollPreviewSerializer(BaseModel):
    id: int
    poll_topic: str

    @classmethod
    def from_orm(cls, poll: PollModel):
        return cls(id=poll.poll_id, poll_topic=poll.poll_topic)