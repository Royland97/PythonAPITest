from fastapi import APIRouter, Depends, HTTPException
from app.core.data_access.i_repository.i_user_repository import IUserRepository
from app.infrastructure.providers import get_user_repository
from app.api.models.user_dto import UserDto, user_to_dto, dto_to_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserDto])
async def get_users(repo: IUserRepository = Depends(get_user_repository)):
    users = await repo.get_all_async()
    return [user_to_dto(u) for u in users]

@router.get("/{id}", response_model=UserDto)
async def get_user(id: str, repo: IUserRepository = Depends(get_user_repository)):
    user = await repo.get_by_id_async(id)
    if not user:
        raise HTTPException(404, "User not found")
    return user_to_dto(user)

@router.post("/", response_model=UserDto)
async def create_user(userDto: UserDto, repo: IUserRepository = Depends(get_user_repository)):
    doc = dto_to_user(userDto)
    created = await repo.save_async(doc)
    return user_to_dto(created)

@router.put("/{id}", response_model=UserDto)
async def update_user(id: str, userDto: UserDto, repo: IUserRepository = Depends(get_user_repository)):
    existing = await repo.get_by_id_async(id)
    if not existing:
        raise HTTPException(404, "User not found")

    updated_data = dto_to_user(userDto)
    updated = {**existing, **updated_data} if isinstance(existing, dict) else {**existing.model_dump(), **updated_data}
    await repo.update_async(updated)
    return user_to_dto(updated)

@router.delete("/{id}")
async def delete_user(id: str, repo: IUserRepository = Depends(get_user_repository)):
    existing = await repo.get_by_id_async(id)
    if not existing:
        raise HTTPException(404, "User not found")
    
    await repo.delete_by_id_async(id)
    return {"message": "User deleted"}
