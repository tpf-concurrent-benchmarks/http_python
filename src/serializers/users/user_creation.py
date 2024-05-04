from pydantic import BaseModel

class UserCreationSerializer(BaseModel):
    username: str
    password: str