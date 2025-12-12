from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.core.domain.objectid_handler import PyObjectId

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            PyObjectId: lambda v: str(v)
        }
    }   
