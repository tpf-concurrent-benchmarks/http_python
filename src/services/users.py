from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.models.users import UserModel
from src.serializers.users.full_user import FullUserSerializer
from src.serializers.users.user_creation import UserCreationSerializer

class UsersService:
    async def get_user(self, db: AsyncSession, user_id: int) -> FullUserSerializer | None:
        user = await UserModel.find(db, user_id)
        if not user:
            return None
        return FullUserSerializer.from_orm(user)
    
    async def create_user(self, db: AsyncSession, user_serializer: UserCreationSerializer) -> FullUserSerializer | None:
        try:
            user = await UserModel.create(db, user_serializer.username, user_serializer.password)
        except IntegrityError:
            return None
        return FullUserSerializer.from_orm(user)
    
    async def get_authenticated(self, db: AsyncSession, username: str, password: str) -> FullUserSerializer | None:
        user = await UserModel.find_by_username(db, username)
        if not user or not user.authenticate(password):
            return None
        return FullUserSerializer.from_orm(user)
    
users_service = UsersService()