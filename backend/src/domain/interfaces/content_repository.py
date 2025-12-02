from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.content import Content, ContentType


class IContentRepository(ABC):
    """Repository Interface für Content-Operationen"""

    @abstractmethod
    async def get_all(self, user_id: str) -> List[Content]:
        """Holt alle Contents eines Users"""
        pass

    @abstractmethod
    async def get_by_id(self, content_id: str, user_id: str) -> Optional[Content]:
        """Holt einen Content by ID (nur wenn er dem User gehört)"""
        pass

    @abstractmethod
    async def get_by_type(self, user_id: str, content_type: ContentType) -> List[Content]:
        """Holt alle Contents eines bestimmten Typs für einen User"""
        pass

    @abstractmethod
    async def create(self, content: Content) -> Content:
        """Erstellt einen neuen Content"""
        pass

    @abstractmethod
    async def update(self, content_id: str, user_id: str, **kwargs) -> Content:
        """Updated einen Content"""
        pass

    @abstractmethod
    async def delete(self, content_id: str, user_id: str) -> None:
        """Löscht einen Content"""
        pass
