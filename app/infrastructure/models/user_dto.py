from pydantic import BaseModel, EmailStr
from typing import Optional

class UserDto(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: str

def user_to_dto(user: dict) -> UserDto:
    if isinstance(user, dict):
        data = dict(user)
    else:
        data = user.model_dump()
    
    # Trun _id ObjectId into string
    if "_id" in data and data["_id"] is not None:
        data["id"] = str(data["_id"])
    #data.pop("_id", None)
    
    return UserDto(**data)

def dto_to_user(dto: UserDto) -> dict:
    data = dto.model_dump(exclude={"id"})
    return data