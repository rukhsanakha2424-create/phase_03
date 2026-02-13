import asyncio
import traceback
from sqlmodel import Session
from app.db.session import get_session

def test_get_session():
    """Test if we can get a database session"""
    print("Testing database session...")
    try:
        session_gen = get_session()
        session = next(session_gen)
        print("Database session acquired successfully")
        session.close()
        print("Database session closed successfully")
        return True
    except Exception as e:
        print(f"Database session error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_get_session()