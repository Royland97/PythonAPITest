from pydantic import BaseModel
from typing import Optional

class SocialDto(BaseModel):
    id: Optional[str] = None
    x: str
    youtube: str
    instagram: str
    linkedin: str
    mastodon: str
    bluesky: str