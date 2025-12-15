from fastapi import Depends
from app.infrastructure.database import get_database
from app.infrastructure.data_access.repository.user_repository import UserRepository
from app.core.data_access.i_repository.i_user_repository import IUserRepository
from app.core.data_access.i_repository.spaceflightnews.i_article_repository import IArticleRepository
from app.core.data_access.i_repository.spaceflightnews.i_report_repository import IReportRepository
from app.infrastructure.data_access.repository.spaceflightnews.article_repository import ArticleRepository
from app.infrastructure.data_access.repository.spaceflightnews.report_repository import ReportRepository

def get_user_repository(db = Depends(get_database)) -> IUserRepository:
    return UserRepository(db)

def get_article_repository(db = Depends(get_database)) -> IArticleRepository:
    return ArticleRepository(db)

def get_report_repository(db = Depends(get_database)) -> IReportRepository:
    return ReportRepository(db)
