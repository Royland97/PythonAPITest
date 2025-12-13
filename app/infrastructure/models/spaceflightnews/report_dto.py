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

def report_to_dto(report: dict) -> ReportDto:
    if isinstance(report, dict):
        data = dict(report)
    else:
        data = report.model_dump()
    
    # Trun _id ObjectId into string
    if "_id" in data and data["_id"] is not None:
        data["id"] = str(data["_id"])
    
    return ReportDto(**data)

def dto_to_report(dto: ReportDto) -> dict:
    data = dto.model_dump(exclude={"id"})
    return data

def response_to_dto(raw: dict) -> ReportDto:
    return ReportDto(
        external_id=raw["id"],
        title=raw["title"],
        authors=[
            AuthorDto(name=a["name"])
            for a in raw.get("authors", [])
        ] or None,
        url=raw["url"],
        image_url=raw["image_url"],
        news_site=raw["news_site"],
        summary=raw["summary"],
        published_at=raw["published_at"],
        updated_at=raw["updated_at"]
    )