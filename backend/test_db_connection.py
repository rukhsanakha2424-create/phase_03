"""Test script to verify database connection to Neon PostgreSQL"""

import asyncio
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import get_settings

async def test_async_connection():
    """Test async connection to Neon PostgreSQL"""
    settings = get_settings()
    print(f"Testing async connection to: {settings.database_url}")
    
    try:
        # Create async engine
        engine = create_async_engine(
            str(settings.database_url),
            echo=True,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=300,
            pool_timeout=30,
        )
        
        # Test the connection
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"Async connection successful: {result.fetchone()}")
            
        await engine.dispose()
        print("Async connection test completed successfully")
        return True
        
    except Exception as e:
        print(f"Async connection failed: {e}")
        return False

def test_sync_connection():
    """Test sync connection to Neon PostgreSQL"""
    settings = get_settings()
    print(f"Testing sync connection to: {settings.database_url}")
    
    try:
        # Create sync engine
        engine = create_engine(
            str(settings.database_url),
            echo=True,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=300,
            pool_timeout=30,
        )
        
        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"Sync connection successful: {result.fetchone()}")
            
        print("Sync connection test completed successfully")
        return True
        
    except Exception as e:
        print(f"Sync connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting database connection tests...")
    
    # Test sync connection
    sync_success = test_sync_connection()
    
    # Test async connection
    async def run_async_test():
        return await test_async_connection()
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        async_success = loop.run_until_complete(run_async_test())
    except Exception as e:
        print(f"Error running async test: {e}")
        async_success = False
    
    print(f"\nResults:")
    print(f"Sync connection: {'SUCCESS' if sync_success else 'FAILED'}")
    print(f"Async connection: {'SUCCESS' if async_success else 'FAILED'}")
    
    if not sync_success and not async_success:
        print("\nBoth connections failed. Please check your database configuration.")
        sys.exit(1)
    else:
        print("\nAt least one connection type succeeded.")
        sys.exit(0)