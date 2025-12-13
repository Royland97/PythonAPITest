from pydantic import BaseModel
from typing import List, Optional
from app.infrastructure.models.spaceflightnews.article_dto import ArticleDto

class ArticlePaginatedDto(BaseModel):
    total: int
    items: Optional[List[ArticleDto]] = None
