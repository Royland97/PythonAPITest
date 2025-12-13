from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.data_access.i_repository.spaceflightnews.i_report_repository import IReportRepository
from app.infrastructure.data_access.repository.mongo_generic_repository import MongoGenericRepository
from typing import Optional

class ReportRepository(MongoGenericRepository, IReportRepository):
    """
    Specific repository with custom queries for Report.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "reports")
    
    # Get report by url
    async def get_by_url_async(self, url: str) -> Optional[dict]:
        return await self.collection.find_one({"url": url})