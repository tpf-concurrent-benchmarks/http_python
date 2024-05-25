from pydantic import BaseModel
from typing import List

from src.models.polls import PollModel

class PollCreationSerializer(BaseModel):
    title: str
    options: List[str]
