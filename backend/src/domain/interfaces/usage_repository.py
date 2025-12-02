from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from ..entities.usage import Usage
from ..entities.content import ContentType


class IUsageRepository(ABC):
    """Repository Interface für Usage-Tracking"""

    @abstractmethod
    async def get_current_usage(
        self,
        user_id: str,
        content_type: ContentType,
        period_start: datetime,
        period_end: datetime
    ) -> Usage:
        """Holt die aktuelle Usage für einen Content-Typ im gegebenen Zeitraum. Returns default Usage with count=0 if none exists."""
        pass

    @abstractmethod
    async def create(self, usage: Usage) -> Usage:
        """Erstellt einen neuen Usage-Eintrag"""
        pass

    @abstractmethod
    async def increment_usage(
        self,
        user_id: str,
        content_type: ContentType,
        period_start: datetime,
        period_end: datetime
    ) -> Usage:
        """Erhöht den Usage-Counter für einen Content-Typ"""
        pass

    @abstractmethod
    async def reset_usage(self, user_id: str) -> None:
        """Setzt alle Usage-Counter für einen User zurück (monatlicher Reset)"""
        pass
