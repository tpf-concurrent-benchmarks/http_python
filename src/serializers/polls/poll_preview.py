from pydantic import BaseModel
from src.models.polls import PollModel

class PollPreviewSerializer(BaseModel):
    id: int
    title: str

    @classmethod
    def from_orm(cls, poll: PollModel):
        return cls(id=poll.poll_id, title=poll.poll_topic)