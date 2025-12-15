from typing import Optional
from abc import ABC, abstractmethod
from app.core.data_access.i_repository.i_mongo_generic_repository import IMongoGenericRepository

class IUserRepository(ABC, IMongoGenericRepository):

    @abstractmethod
    async def get_by_email_async(self, email: str) -> Optional[dict]:
        ...
