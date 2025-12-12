from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.data_access.i_repository.i_user_repository import IUserRepository
from app.infrastructure.data_access.repository.mongo_generic_repository import MongoGenericRepository

class UserRepository(MongoGenericRepository, IUserRepository):
    """
    Specific repository with custom queries for User.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "users")

    # Get user by email
    async def get_by_email_async(self, email: str) -> Optional[dict]:
        return await self.collection.find_one({"email": email})
