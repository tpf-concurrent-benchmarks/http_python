from pydantic import BaseModel

class PollCreationOutputSerializer(BaseModel):
    id: int