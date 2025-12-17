from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.user_router import router as user_router
from app.api.routers.auth_router import router as auth_router
from app.api.routers.spaceflightnews.article_router import router as article_router
from app.api.routers.spaceflightnews.report_router import router as report_router
from app.infrastructure.database import connect_db, close_db
from contextlib import asynccontextmanager

# ------------------------
# MongoDB Connection
# ------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup
    await connect_db()
    yield
    #Shutdown
    await close_db()

# ------------------------
# FastAPI app
# ------------------------
app = FastAPI(
    title="FastAPI MongoDB Clean Architecture",
    description="""
    The API consumes information from **SpaceflightNewsAPI**

    URL: https://www.spaceflightnewsapi.net/
    """,
    version="1.1.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Routers
# ------------------------
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(article_router)
app.include_router(report_router)
