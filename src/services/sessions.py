from sqlalchemy.orm import Session

from src.services.users import users_service
from src.helpers.jwt import jwt_manager
from src.serializers.token import TokenSerializer
from src.serializers.users.user_creation import UserCreationSerializer

class SessionsService:
    def create_token(self, db: Session, user_serializer: UserCreationSerializer) -> TokenSerializer | None:
        user = users_service.get_authenticated(db, user_serializer.username, user_serializer.password)
        if not user:
            return None
        token_str = jwt_manager.create_jwt_token({"user_id": user.user_id})
        return TokenSerializer(access_token=token_str, token_type="bearer")
    
    def create_token_for(self, user_id: int) -> str:
        token_str = jwt_manager.create_jwt_token({"user_id": user_id})
        return TokenSerializer(access_token=token_str, token_type="bearer")
    
    def get_user_id(self, token: str) -> int:
        decoded_token = jwt_manager.decode_jwt_token(token)
        if not decoded_token or "user_id" not in decoded_token:
            raise ValueError("Invalid token")
        return decoded_token["user_id"]

sessions_service = SessionsService()