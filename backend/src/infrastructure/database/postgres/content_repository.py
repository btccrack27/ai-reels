from typing import List, Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.interfaces.content_repository import IContentRepository
from ....domain.entities.content import Content, ContentType, ContentStatus
from .models import ContentModel


class PostgresContentRepository(IContentRepository):
    """
    Postgres Implementation des Content Repository.
    Verwendet Vercel Postgres (Neon) via asyncpg.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, user_id: str) -> List[Content]:
        """Holt alle Contents eines Users"""
        stmt = select(ContentModel).where(
            ContentModel.user_id == user_id
        ).order_by(ContentModel.created_at.desc())

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    async def get_by_id(self, content_id: str, user_id: str) -> Optional[Content]:
        """Holt einen Content by ID (nur wenn er dem User gehört)"""
        stmt = select(ContentModel).where(
            ContentModel.id == content_id,
            ContentModel.user_id == user_id
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        return self._to_entity(model) if model else None

    async def get_by_type(self, user_id: str, content_type: ContentType) -> List[Content]:
        """Holt alle Contents eines bestimmten Typs für einen User"""
        stmt = select(ContentModel).where(
            ContentModel.user_id == user_id,
            ContentModel.type == content_type.value
        ).order_by(ContentModel.created_at.desc())

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [self._to_entity(model) for model in models]

    async def create(self, content: Content) -> Content:
        """Erstellt einen neuen Content"""
        model = ContentModel(
            id=content.id,
            user_id=content.user_id,
            type=content.type.value,
            status=content.status.value,
            data=content.data,
            prompt=content.prompt,
            version=content.version,
            metadata=content.metadata,
            created_at=content.created_at,
            updated_at=content.updated_at
        )

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return self._to_entity(model)

    async def update(self, content_id: str, user_id: str, **kwargs) -> Content:
        """Updated einen Content"""
        stmt = select(ContentModel).where(
            ContentModel.id == content_id,
            ContentModel.user_id == user_id
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            raise ValueError(f"Content {content_id} nicht gefunden")

        # Update fields
        for key, value in kwargs.items():
            if hasattr(model, key):
                # Handle enum values
                if key in ['type', 'status'] and hasattr(value, 'value'):
                    setattr(model, key, value.value)
                else:
                    setattr(model, key, value)

        model.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(model)

        return self._to_entity(model)

    async def delete(self, content_id: str, user_id: str) -> None:
        """Löscht einen Content"""
        stmt = select(ContentModel).where(
            ContentModel.id == content_id,
            ContentModel.user_id == user_id
        )

        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.commit()

    def _to_entity(self, model: ContentModel) -> Content:
        """Konvertiert SQLAlchemy Model zu Domain Entity"""
        return Content(
            id=str(model.id),
            user_id=str(model.user_id),
            type=ContentType(model.type),
            status=ContentStatus(model.status),
            data=model.data,
            prompt=model.prompt,
            version=model.version,
            metadata=model.metadata,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
