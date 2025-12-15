from typing import TypeVar, Iterable, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.core.data_access.i_repository.i_mongo_generic_repository import IMongoGenericRepository

TEntity = TypeVar("TEntity")

# Generic Repository using MongoDB
class MongoGenericRepository(IMongoGenericRepository):
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.collection = db[collection_name]

    # ---------------------------
    # Save
    # ---------------------------
    async def save_async(self, entity: dict) -> dict:
        result = await self.collection.insert_one(entity)
        entity["_id"] = result.inserted_id
        return entity

    async def save_all_async(self, entities: Iterable[dict]) -> List[dict]:
        for entity in entities:
            await self.save_async(entity)
        return entities

    # ---------------------------
    # Update
    # ---------------------------
    async def update_async(self, entity: dict) -> dict:
        if "_id" not in entity:
            raise ValueError("Entity must contain '_id' field for update")

        await self.collection.replace_one({"_id": entity["_id"]}, entity)
        return entity

    async def update_all_async(self, entities: Iterable[dict]) -> List[dict]:
        for entity in entities:
            await self.update_async(entity)
        return list(entities)

    # ---------------------------
    # Delete
    # ---------------------------
    async def delete_async(self, entity: dict) -> None:
        await self.collection.delete_one({"_id": entity["_id"]})

    async def delete_all_async(self, entities: Iterable[dict]) -> None:
        for entity in entities:
            await self.delete_async(entity)

    async def delete_by_id_async(self, id: str) -> None:
        oid = ObjectId(id)
        result = await self.collection.delete_one({"_id": oid})

        if result.deleted_count == 0:
            raise ValueError(f"Entity with id {id} does not exist")

    # ---------------------------
    # Get
    # ---------------------------
    async def get_by_id_async(self, id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def get_all_async(self) -> List[dict]:
        docs = self.collection.find({})
        return [doc async for doc in docs]

    async def get_all_by_ids_async(self, ids: Iterable[str]) -> List[dict]:
        oid_list = [ObjectId(id) for id in ids]
        docs = self.collection.find({"_id": {"$in": oid_list}})
        return [doc async for doc in docs]
    
    async def get_paginated_async(
        self,
        skip: int,
        limit: int,
        sort: tuple = ("_id", -1)
    ) -> tuple[int, List[dict]]:
        total = await self.collection.count_documents({})
        cursor = (
            self.collection
            .find({})
            .sort(sort[0], sort[1])
            .skip(skip)
            .limit(limit)
        )

        items = await cursor.to_list(length=limit)
        return total, items

