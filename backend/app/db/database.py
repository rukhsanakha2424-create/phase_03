"""Database configuration for SQLite or PostgreSQL"""

from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import get_settings

settings = get_settings()

# Determine if we're using PostgreSQL or SQLite
database_url_str = str(settings.database_url)

if database_url_str.startswith("postgresql"):
    # PostgreSQL setup
    # Create sync engine for PostgreSQL (using psycopg2 connection string with sqlmodel)
    sync_engine = create_engine(
        database_url_str,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300,
        pool_timeout=30,
    )

    # Create async engine for PostgreSQL - using asyncpg driver
    async_database_url = database_url_str.replace("postgresql://", "postgresql+asyncpg://")
elif database_url_str.startswith("sqlite"):
    # SQLite setup
    # For SQLite, we need to handle both regular and async versions
    if "aiosqlite" in database_url_str:
        # If it's the async version, convert to sync
        sync_url = database_url_str.replace("+aiosqlite:", ":")
    else:
        # If it's already sync, use as-is
        sync_url = database_url_str
    
    sync_engine = create_engine(
        sync_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300,
        pool_timeout=30,
    )
    async_database_url = database_url_str
else:
    # Default to SQLite
    sync_engine = create_engine(
        "sqlite:///./test.db",
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_recycle=300,
        pool_timeout=30,
    )
    async_database_url = "sqlite+aiosqlite:///./test.db"

# Create async engine
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