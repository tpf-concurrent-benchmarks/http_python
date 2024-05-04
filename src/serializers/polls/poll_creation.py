from pydantic import BaseModel
from typing import List

from src.serializers.poll_options.poll_option_creation import PollOptionCreationSerializer

class PollCreationSerializer(BaseModel):
    poll_topic: str
    options: List[PollOptionCreationSerializer]
