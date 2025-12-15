from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import db_settings

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(db_settings.mongo_url)
    db = client[db_settings.database]
    print(f"MongoDB connected: {db_settings.mongo_url}")

async def close_db():
    global client
    client.close()  
    print("MongoDB disconnected")

def get_database()-> AsyncIOMotorDatabase:
    return db
