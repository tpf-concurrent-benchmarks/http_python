from pydantic import BaseModel

class FullUserSerializer(BaseModel):
    user_id: int
    username: str
    hashed_password: str

    class Config:
        orm_mode = True