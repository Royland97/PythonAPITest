import asyncio
import httpx
from app.infrastructure.services.spaceflightnews.article_sync_progress import progress
from app.infrastructure.models.spaceflightnews.article_dto import response_to_dto, dto_to_article
from app.core.data_access.i_repository.spaceflightnews.i_article_repository import IArticleRepository

SPACEFLIGHT_API_URL = "https://api.spaceflightnewsapi.net/v4/articles/"
REQUEST_DELAY = 0.4  # ~2.5 req/seg

async def sync_all_articles(repo: IArticleRepository):
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

                articles_to_insert = []

                for raw in data.get("results", []):
                    dto = response_to_dto(raw)

                    if await repo.get_by_url_async(dto.url):
                        continue

                    articles_to_insert.append(dto_to_article(dto))

                if articles_to_insert:
                    await repo.save_all_async(articles_to_insert)
                    progress.saved += len(articles_to_insert)

                await asyncio.sleep(REQUEST_DELAY)
            
            # Create indexes
            await create_article_indexes(repo)

        except Exception as ex:
            progress.error = str(ex)

        finally:
            progress.running = False

async def create_article_indexes(repo: IArticleRepository):
    """
    Creates the necessary indexes in MongoDB for the articles collection.
    It only runs once at the end of the synchronization.
    """
    collection = repo.collection
    await collection.create_index("url", unique=True)