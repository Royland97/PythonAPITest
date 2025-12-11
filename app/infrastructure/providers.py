from fastapi import Depends
from app.infrastructure.database import get_database
from app.infrastructure.data_access.repository.user_repository import UserRepository
from app.core.data_access.i_repository.i_user_repository import IUserRepository

def get_user_repository(db = Depends(get_database)) -> IUserRepository:
    return UserRepository(db)
