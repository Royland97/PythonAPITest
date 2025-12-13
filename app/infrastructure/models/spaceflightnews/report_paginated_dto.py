from pydantic import BaseModel
from typing import List, Optional
from app.infrastructure.models.spaceflightnews.report_dto import ReportDto

class ReportPaginatedDto(BaseModel):
    total: int
    items: Optional[List[ReportDto]] = None
