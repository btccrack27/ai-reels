import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Vercel Postgres Connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/reels_db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # SQL logging (disable in production)
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base for models
Base = declarative_base()


async def get_session() -> AsyncSession:
    """
    Dependency für FastAPI Endpoints.
    Liefert eine DB-Session.
    """
    async with async_session_maker() as session:
        yield session


async def init_db():
    """
    Initialisiert die Datenbank.
    Erstellt alle Tabellen (falls nicht vorhanden).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Schließt die Datenbank-Verbindung"""
    await engine.dispose()
