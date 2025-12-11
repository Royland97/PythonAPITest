from typing import Protocol, List, Optional
from app.core.domain.user import User

class IUserRepository(Protocol):
    """
    Interfaz para UserRepository usando Pydantic User.
    """

    async def save_async(self, user: User) -> User:
        ...

    async def get_by_id_async(self, id: str) -> Optional[User]:
        ...

    async def get_all_async(self) -> List[User]:
        ...

    async def update_async(self, user: User) -> User:
        ...

    async def delete_by_id_async(self, id: str) -> None:
        ...

    async def get_by_email_async(self, email: str) -> Optional[User]:
        ...
