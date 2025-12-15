import asyncio
import httpx
from app.infrastructure.services.spaceflightnews.sync_progress import progress
from app.infrastructure.models.spaceflightnews.report_dto import response_to_dto, dto_to_report
from app.core.data_access.i_repository.spaceflightnews.i_report_repository import IReportRepository

SPACEFLIGHT_API_URL = "https://api.spaceflightnewsapi.net/v4/reports/"
REQUEST_DELAY = 0.4  # ~2.5 req/seg

async def sync_all_reports(repo: IReportRepository):
    if progress.running:
        return

    progress.running = True
    progress.current_page = 0
    progress.saved = 0
    progress.total = None
    progress.error = None

    url = SPACEFLIGHT_API_URL

    async with httpx.AsyncClient(verify=False, timeout=30) as client:
        try:
            while url and not progress.cancelled:

                response = await client.get(url)

                # Rate limit / retry
                if response.status_code == 429:
                    await asyncio.sleep(2)
                    continue

                response.raise_for_status()
                data = response.json()

                progress.total = data.get("count")
                progress.current_page += 1
                url = data.get("next")

                reports_to_insert = []

                for raw in data.get("results", []):
                    dto = response_to_dto(raw)

                    if await repo.get_by_url_async(dto.url):
                        continue

                    reports_to_insert.append(dto_to_report(dto))

                if reports_to_insert:
                    await repo.save_all_async(reports_to_insert)
                    progress.saved += len(reports_to_insert)

                await asyncio.sleep(REQUEST_DELAY)
            
            # Create indexes
            await create_report_indexes(repo)

        except Exception as ex:
            progress.error = str(ex)

        finally:
            progress.running = False

async def create_report_indexes(repo: IReportRepository):
    """
    Creates the necessary indexes in MongoDB for the reports collection.
    It only runs once at the end of the synchronization.
    """
    collection = repo.collection
    await collection.create_index("url", unique=True)