from pydantic import BaseModel
from typing import List

class PollCreationSerializer(BaseModel):
    poll_topic: str
    options: List[str]
