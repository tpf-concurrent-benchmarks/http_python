from fastapi import APIRouter, HTTPException


from src.services.sessions import sessions_service
from src.helpers.dependencies import DbDependency
from src.serializers.token import TokenSerializer
from src.serializers.users.user_creation import UserCreationSerializer

router = APIRouter()


@router.post("/api/login", response_model=TokenSerializer)
async def login_for_token(user_serializer: UserCreationSerializer,
                          db: DbDependency):
    token = await sessions_service.create_token(db, user_serializer)
    if not token:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return token
