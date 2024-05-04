from sqlalchemy.orm import Session

from src.models.users import UserModel
from src.serializers.users.full_user import FullUserSerializer

class UsersService:
    def get_user(self, db: Session, user_id: int) -> FullUserSerializer | None:
        user = UserModel.find(db, user_id)
        if not user:
            return None
        return FullUserSerializer.from_orm(user)
    
    def create_user(self, db: Session, username: str, password: str) -> FullUserSerializer | None:
        user = UserModel.find_by_username(db, username)
        if user:
            return None
        user = UserModel.create(db, username, password)
        return FullUserSerializer.from_orm(user)
    
    def get_authenticated(self, db: Session, username: str, password: str) -> FullUserSerializer | None:
        user = UserModel.find_by_username(db, username)
        if not user or not user.authenticate(password):
            return None
        return FullUserSerializer.from_orm(user)
    
users_service = UsersService()