from pydantic import BaseModel
from typing import List

from src.serializers.polls.poll_creation import PollCreationSerializer

class PollCreationOutputSerializer(PollCreationSerializer):
    poll_id: str