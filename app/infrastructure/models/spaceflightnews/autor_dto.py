from pydantic import BaseModel
from typing import Optional
from app.infrastructure.models.spaceflightnews.social_dto import SocialDto

class AuthorDto(BaseModel):
    id: Optional[str] = None
    name: str
    socials: Optional[SocialDto] = None

def author_to_dto(author: dict) -> AuthorDto:
    if isinstance(author, dict):
        data = dict(author)
    else:
        data = author.model_dump()
    
    # Trun _id ObjectId into string
    if "_id" in data and data["_id"] is not None:
        data["id"] = str(data["_id"])
    
    return AuthorDto(**data)

def dto_to_author(dto: AuthorDto) -> dict:
    data = dto.model_dump(exclude={"id"})
    return data