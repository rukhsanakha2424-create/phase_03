import asyncio
from sqlmodel import Session, SQLModel
from app.db.database import async_engine
from app.api.v1.agent import get_agent_status
from app.db.session import get_session

async def test_agent_status():
    # Create tables first
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Get a session
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        result = await get_agent_status(session)
        print(f"Agent status result: {result}")
    except Exception as e:
        print(f"Error getting agent status: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent_status())