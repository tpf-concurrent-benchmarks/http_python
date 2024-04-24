from src.models.user import UserInDB
from src.database.database import DataBase

class InMemoryDataBase(DataBase):
    def __init__(self):
        self.users = {}

    async def get_user(self, username: str) -> UserInDB | None:
        if username in self.users:
            user_dict = self.users[username]
            return UserInDB(**user_dict)
        return None
    
    async def add_user(self, user: UserInDB) -> bool:
        if user.username in self.users:
            return False
        self.users[user.username] = user.dict()
        return True