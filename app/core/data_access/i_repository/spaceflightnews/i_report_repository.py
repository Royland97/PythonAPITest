from typing import Optional
from abc import ABC, abstractmethod
from app.core.data_access.i_repository.i_mongo_generic_repository import IMongoGenericRepository

class IReportRepository(ABC, IMongoGenericRepository):
    
    @abstractmethod
    async def get_by_url_async(self, url: str) -> Optional[dict]:
        ...