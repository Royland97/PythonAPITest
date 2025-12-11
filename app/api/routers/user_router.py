from fastapi import APIRouter, Depends, HTTPException
from app.core.data_access.i_repository.i_user_repository import IUserRepository
from app.infrastructure.providers import get_user_repository
from app.core.domain.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[User])
async def get_users(repo: IUserRepository = Depends(get_user_repository)):
    return await repo.get_all_async()


@router.get("/{id}", response_model=User)
async def get_user(id: str, repo: IUserRepository = Depends(get_user_repository)):
    user = await repo.get_by_id_async(id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.post("/", response_model=User)
async def create_user(user: User, repo: IUserRepository = Depends(get_user_repository)):
    doc = {"name": user.name, "email": user.email}
    return await repo.save_async(doc)


@router.put("/{id}", response_model=User)
async def update_user(id: str, user: User, repo: IUserRepository = Depends(get_user_repository)):
    existing = await repo.get_by_id_async(id)
    if not existing:
        raise HTTPException(404, "User not found")

    updated = {**existing, **user.model_dump(exclude_none=True)}
    await repo.update_async(updated)
    return updated


@router.delete("/{id}")
async def delete_user(id: str, repo: IUserRepository = Depends(get_user_repository)):
    await repo.delete_by_id_async(id)
    return {"message": "User deleted"}
