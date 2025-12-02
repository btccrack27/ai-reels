from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.interfaces.subscription_repository import ISubscriptionRepository
from ....domain.entities.subscription import Subscription, SubscriptionPlan, SubscriptionStatus
from .models import SubscriptionModel


class PostgresSubscriptionRepository(ISubscriptionRepository):
    """Postgres Implementation des Subscription Repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: str) -> Optional[Subscription]:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.user_id == user_id,
            SubscriptionModel.status.in_(['active', 'trialing'])
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_stripe_id(self, stripe_subscription_id: str) -> Optional[Subscription]:
        stmt = select(SubscriptionModel).where(
            SubscriptionModel.stripe_subscription_id == stripe_subscription_id
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def create(self, subscription: Subscription) -> Subscription:
        model = SubscriptionModel(
            id=subscription.id,
            user_id=subscription.user_id,
            plan=subscription.plan.value,
            status=subscription.status.value,
            stripe_subscription_id=subscription.stripe_subscription_id,
            current_period_start=subscription.current_period_start,
            current_period_end=subscription.current_period_end,
            cancel_at_period_end=subscription.cancel_at_period_end
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def update(self, subscription_id: str, **kwargs) -> Subscription:
        stmt = select(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            raise ValueError(f"Subscription {subscription_id} nicht gefunden")

        for key, value in kwargs.items():
            if hasattr(model, key):
                if key in ['plan', 'status'] and hasattr(value, 'value'):
                    setattr(model, key, value.value)
                else:
                    setattr(model, key, value)

        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, subscription_id: str) -> None:
        stmt = select(SubscriptionModel).where(SubscriptionModel.id == subscription_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.commit()

    def _to_entity(self, model: SubscriptionModel) -> Subscription:
        return Subscription(
            id=str(model.id),
            user_id=str(model.user_id),
            plan=SubscriptionPlan(model.plan),
            status=SubscriptionStatus(model.status),
            stripe_subscription_id=model.stripe_subscription_id,
            current_period_start=model.current_period_start,
            current_period_end=model.current_period_end,
            cancel_at_period_end=model.cancel_at_period_end
        )
