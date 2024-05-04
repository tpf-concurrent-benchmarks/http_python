from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from src.database import get_db
from src.helpers.authentication import authenticate_with_jwt

AuthDependency = Annotated[int, Depends(authenticate_with_jwt)]
DbDependency = Annotated[Session, Depends(get_db)]