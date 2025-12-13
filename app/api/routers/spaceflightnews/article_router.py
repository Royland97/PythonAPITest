from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.data_access.i_repository.spaceflightnews.i_article_repository import IArticleRepository
from app.infrastructure.providers import get_article_repository
from app.infrastructure.models.spaceflightnews.article_dto import article_to_dto 
from app.infrastructure.models.spaceflightnews.article_paginated_dto import ArticlePaginatedDto 
from app.api.tools.security_token import get_current_user
from app.infrastructure.services.spaceflightnews.article_progress import progress
from app.infrastructure.services.spaceflightnews.article_services import sync_all_articles
import asyncio

router = APIRouter(prefix="/articles", tags=["Article"])

# ---------- SYNC ----------
@router.post("/sync")
async def start_sync(
    repo: IArticleRepository = Depends(get_article_repository)
    #current_user=Depends(get_current_user)
):
    if progress.running:
        raise HTTPException(409, "La sincronización ya está en ejecución")

    asyncio.create_task(sync_all_articles(repo))

    return {"message": "Sincronización iniciada"}

# ---------- SYNC PROGRESS ----------
@router.get("/sync/progress")
async def get_sync_progress(
    #current_user=Depends(get_current_user)
):
    return {
        "running": progress.running,
        "cancelled": progress.cancelled,
        "current_page": progress.current_page,
        "articles_saved": progress.saved,
        "total_articles": progress.total,
        "error": progress.error
    }

# ---------- CANCEL SYNC ----------
@router.post("/sync/cancel")
async def cancel_sync():
    progress.cancelled = True


# ---------- GET PAGINATED ----------
@router.get("/", response_model=ArticlePaginatedDto)
async def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    repo: IArticleRepository = Depends(get_article_repository)
    #current_user=Depends(get_current_user)
):
    skip = (page - 1) * page_size
    total, articles = await repo.get_paginated_async(skip, page_size)

    return {
        "total": total,
        "items": [article_to_dto(a) for a in articles]
    }
