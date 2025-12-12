from fastapi import APIRouter, Depends, HTTPException
from app.api.models.auth_dto import LoginDto, TokenResponse
from app.core.security import verify_password, create_access_token
from app.infrastructure.providers import get_user_repository
from app.api.models.user_dto import user_to_dto

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
async def login(dto: LoginDto, repo=Depends(get_user_repository)):

    user = await repo.get_by_email_async(dto.email)
    userDto = user_to_dto(user)
    if not userDto:
        raise HTTPException(401, "Invalid credentials")

    if not verify_password(dto.password, userDto.password):
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token({"sub": str(userDto.id)})

    return TokenResponse(access_token=access_token)
