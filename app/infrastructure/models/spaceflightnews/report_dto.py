from pydantic import BaseModel
from typing import Optional, List
from app.infrastructure.models.spaceflightnews.autor_dto import AuthorDto

class ReportDto(BaseModel):
    id: Optional[str] = None
    external_id: int
    title: str
    authors: Optional[List[AuthorDto]] = None
    url: str
    image_url: str
    news_site: str
    summary: str
    published_at: str
    updated_at: str