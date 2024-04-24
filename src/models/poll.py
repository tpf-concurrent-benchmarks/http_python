from pydantic import BaseModel
from typing import List

class Poll(BaseModel):
    title: str
    options: List[str]