from pydantic import BaseModel

class PollOptionCreationSerializer(BaseModel):
    name: str