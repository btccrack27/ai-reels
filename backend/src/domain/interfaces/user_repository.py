from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User


class IUserRepository(ABC):
    """Repository Interface für User-Operationen"""

    @abstractmethod
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """Holt einen User by ID"""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Holt einen User by Email"""
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Erstellt einen neuen User"""
        pass

    @abstractmethod
    async def update(self, user_id: str, **kwargs) -> User:
        """Updated einen User"""
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> None:
        """Löscht einen User"""
        pass
