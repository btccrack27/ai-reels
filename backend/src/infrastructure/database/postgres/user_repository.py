from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ....domain.interfaces.user_repository import IUserRepository
from ....domain.entities.user import User, UserRole
from .models import UserModel


class PostgresUserRepository(IUserRepository):
    """Postgres Implementation des User Repository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def create(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role.value,
            subscription_id=user.subscription_id,
            stripe_customer_id=user.stripe_customer_id,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def update(self, user_id: str, **kwargs) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if not model:
            raise ValueError(f"User {user_id} nicht gefunden")

        for key, value in kwargs.items():
            if hasattr(model, key):
                if key == 'role' and hasattr(value, 'value'):
                    setattr(model, key, value.value)
                else:
                    setattr(model, key, value)

        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def delete(self, user_id: str) -> None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            await self.session.delete(model)
            await self.session.commit()

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=str(model.id),
            email=model.email,
            name=model.name,
            role=UserRole(model.role),
            subscription_id=str(model.subscription_id) if model.subscription_id else None,
            stripe_customer_id=model.stripe_customer_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active
        )
