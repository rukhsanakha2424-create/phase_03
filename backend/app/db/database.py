"""Database configuration for Neon PostgreSQL"""

from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import get_settings

settings = get_settings()

# Create sync engine for PostgreSQL (using psycopg2 connection string with sqlmodel)
sync_engine = create_engine(
    str(settings.database_url),
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
    pool_timeout=30,
)

# Create async engine for PostgreSQL - using asyncpg driver
async_database_url = str(settings.database_url).replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(
    async_database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
    pool_timeout=30,
)

# Create sync session maker
SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

def get_sync_session():
    with SyncSessionLocal() as session:
        yield session

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session