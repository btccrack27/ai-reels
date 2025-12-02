from typing import Optional
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.interfaces.usage_repository import IUsageRepository
from ....domain.entities.usage import Usage
from ....domain.entities.content import ContentType
from .models import UsageTrackingModel


class PostgresUsageRepository(IUsageRepository):
    """Postgres Implementation des Usage Repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_current_usage(
        self,
        user_id: str,
        content_type: ContentType,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Usage]:
        stmt = select(UsageTrackingModel).where(
            and_(
                UsageTrackingModel.user_id == user_id,
                UsageTrackingModel.content_type == content_type.value,
                UsageTrackingModel.period_start == period_start,
                UsageTrackingModel.period_end == period_end
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def create(self, usage: Usage) -> Usage:
        model = UsageTrackingModel(
            id=usage.id,
            user_id=usage.user_id,
            content_type=usage.content_type,
            count=usage.count,
            period_start=usage.period_start,
            period_end=usage.period_end
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def increment_usage(
        self,
        user_id: str,
        content_type: ContentType,
        period_start: datetime,
        period_end: datetime
    ) -> Usage:
        # Try to get existing usage
        usage = await self.get_current_usage(user_id, content_type, period_start, period_end)

        if usage:
            # Update existing
            stmt = select(UsageTrackingModel).where(UsageTrackingModel.id == usage.id)
            result = await self.session.execute(stmt)
            model = result.scalar_one()
            model.count += 1
            await self.session.commit()
            await self.session.refresh(model)
            return self._to_entity(model)
        else:
            # Create new
            import uuid
            new_usage = Usage(
                id=str(uuid.uuid4()),
                user_id=user_id,
                content_type=content_type.value,
                count=1,
                period_start=period_start,
                period_end=period_end
            )
            return await self.create(new_usage)

    async def reset_usage(self, user_id: str) -> None:
        # In practice würde man alte Records archivieren statt löschen
        # Für jetzt: löschen wir alle Usage-Records des Users
        stmt = select(UsageTrackingModel).where(UsageTrackingModel.user_id == user_id)
        result = await self.session.execute(stmt)
        models = result.scalars().all()

        for model in models:
            await self.session.delete(model)

        await self.session.commit()

    def _to_entity(self, model: UsageTrackingModel) -> Usage:
        return Usage(
            id=str(model.id),
            user_id=str(model.user_id),
            content_type=model.content_type,
            count=model.count,
            period_start=model.period_start,
            period_end=model.period_end
        )
