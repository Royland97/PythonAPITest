from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.data_access.i_repository.spaceflightnews.i_report_repository import IReportRepository
from app.infrastructure.data_access.repository.mongo_generic_repository import MongoGenericRepository

class ReportRepository(MongoGenericRepository, IReportRepository):
    """
    Specific repository with custom queries for Report.
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db, "reports")