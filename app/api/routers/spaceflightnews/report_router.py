from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.data_access.i_repository.spaceflightnews.i_report_repository import IReportRepository
from app.infrastructure.providers import get_report_repository
from app.infrastructure.models.spaceflightnews.report_dto import report_to_dto 
from app.infrastructure.models.spaceflightnews.report_paginated_dto import ReportPaginatedDto 
from app.api.tools.security_token import get_current_user
from app.infrastructure.services.spaceflightnews.report_sync_progress import progress
from app.infrastructure.services.spaceflightnews.report_services import sync_all_reports
import asyncio

router = APIRouter(prefix="/reports", tags=["Report"])

# ---------- SYNC ----------
@router.post("/sync")
async def start_sync(
    repo: IReportRepository = Depends(get_report_repository),
    current_user=Depends(get_current_user)
):
    if progress.running:
        raise HTTPException(409, "Synchronization already start")

    asyncio.create_task(sync_all_reports(repo))

    return {"message": "Synchronization start"}

# ---------- SYNC PROGRESS ----------
@router.get("/sync/progress")
async def get_sync_progress(
    current_user=Depends(get_current_user)
):
    return {
        "running": progress.running,
        "cancelled": progress.cancelled,
        "current_page": progress.current_page,
        "reports_saved": progress.saved,
        "total_reports": progress.total,
        "error": progress.error
    }

# ---------- CANCEL SYNC ----------
@router.post("/sync/cancel")
async def cancel_sync(
    current_user=Depends(get_current_user)
):
    progress.cancelled = True
    return {"message": "Synchronization cancelled"}

# ---------- GET PAGINATED ----------
@router.get("/", response_model=ReportPaginatedDto)
async def get_reports(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    repo: IReportRepository = Depends(get_report_repository),
    current_user=Depends(get_current_user)
):
    skip = (page - 1) * page_size
    total, reports = await repo.get_paginated_async(skip, page_size)

    return {
        "total": total,
        "items": [report_to_dto(a) for a in reports]
    }
