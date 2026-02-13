import asyncio
from sqlmodel import SQLModel
from app.db.database import async_engine

async def create_tables():
    print("Creating database tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())