from pydantic import BaseModel

class TokenSerializer(BaseModel):
    access_token: str
    token_type: str