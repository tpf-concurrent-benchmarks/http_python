from pydantic import BaseModel
from typing import List

from src.serializers.polls.poll_preview import PollPreviewSerializer

class AllPollsSerializer(BaseModel):
    polls: List[PollPreviewSerializer]