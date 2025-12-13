from typing import Protocol, Iterable, List, Optional, runtime_checkable

@runtime_checkable
class IMongoGenericRepository(Protocol):

    async def save_async(self, entity: dict) -> dict:
        ...

    async def save_all_async(self, entities: Iterable[dict]) -> List[dict]:
        ...

    async def update_async(self, entity: dict) -> dict:
        ...

    async def update_all_async(self, entities: Iterable[dict]) -> List[dict]:
        ...

    async def delete_async(self, entity: dict) -> None:
        ...

    async def delete_all_async(self, entities: Iterable[dict]) -> None:
        ...

    async def delete_by_id_async(self, id: str) -> None:
        ...

    async def get_by_id_async(self, id: str) -> Optional[dict]:
        ...

    async def get_all_async(self) -> List[dict]:
        ...

    async def get_all_by_ids_async(self, ids: Iterable[str]) -> List[dict]:
        ...

    async def get_paginated_async(
        self,
        skip: int,
        limit: int,
        sort: tuple = ("_id", -1)
    ) -> tuple[int, List[dict]]:
        ...
