from abc import ABC, abstractmethod
from typing import Optional
from ..entities.subscription import Subscription


class ISubscriptionRepository(ABC):
    """Repository Interface für Subscription-Operationen"""

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[Subscription]:
        """Holt die aktive Subscription eines Users"""
        pass

    @abstractmethod
    async def get_by_stripe_id(self, stripe_subscription_id: str) -> Optional[Subscription]:
        """Holt eine Subscription by Stripe ID"""
        pass

    @abstractmethod
    async def create(self, subscription: Subscription) -> Subscription:
        """Erstellt eine neue Subscription"""
        pass

    @abstractmethod
    async def update(self, subscription_id: str, **kwargs) -> Subscription:
        """Updated eine Subscription"""
        pass

    @abstractmethod
    async def delete(self, subscription_id: str) -> None:
        """Löscht eine Subscription"""
        pass
