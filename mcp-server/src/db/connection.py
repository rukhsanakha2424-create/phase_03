"""PostgreSQL database connection pool for MCP Adapter."""

import asyncio
import os
from typing import Optional

import asyncpg


class DatabasePool:
    """Manages asyncpg connection pool for stateless database access."""

    _instance: Optional["DatabasePool"] = None
    _pool: Optional[asyncpg.Pool] = None

    def __new__(cls) -> "DatabasePool":
        """Ensure singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    async def initialize(cls, database_url: Optional[str] = None) -> None:
        """Initialize the connection pool.

        Args:
            database_url: PostgreSQL connection string. If None, reads from DATABASE_URL env var.

        Raises:
            ValueError: If database_url is not provided and DATABASE_URL env var is not set
            asyncpg.CannotConnectNowError: If cannot connect to database
        """
        instance = cls()

        if instance._pool is not None:
            return  # Already initialized

        if database_url is None:
            database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise ValueError("DATABASE_URL environment variable is required")

        # Get pool configuration from environment or use defaults
        pool_min_size = int(os.getenv("DB_POOL_MIN_SIZE", "5"))
        pool_max_size = int(os.getenv("DB_POOL_MAX_SIZE", "20"))
        command_timeout = int(os.getenv("DB_COMMAND_TIMEOUT", "60"))

        instance._pool = await asyncpg.create_pool(
            database_url,
            min_size=pool_min_size,
            max_size=pool_max_size,
            command_timeout=command_timeout,
        )

        print(
            f"Database connection pool initialized "
            f"(min: {pool_min_size}, max: {pool_max_size})"
        )

    @classmethod
    async def close(cls) -> None:
        """Close all connections in the pool."""
        instance = cls()
        if instance._pool is not None:
            await instance._pool.close()
            instance._pool = None
            print("Database connection pool closed")

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        """Get the connection pool instance.

        Returns:
            The asyncpg connection pool

        Raises:
            RuntimeError: If pool has not been initialized
        """
        instance = cls()
        if instance._pool is None:
            raise RuntimeError(
                "Database pool not initialized. Call DatabasePool.initialize() first."
            )
        return instance._pool

    @classmethod
    async def execute(
        cls, query: str, *args, **kwargs
    ) -> Optional[list]:
        """Execute a query and return results (for SELECT).

        Args:
            query: SQL query string
            *args: Query parameters

        Returns:
            List of result rows (empty if no results)

        Raises:
            asyncpg.PostgresError: If query fails
        """
        pool = cls.get_pool()
        async with pool.acquire() as connection:
            return await connection.fetch(query, *args)

    @classmethod
    async def execute_one(cls, query: str, *args) -> Optional[dict]:
        """Execute a query and return a single row.

        Args:
            query: SQL query string
            *args: Query parameters

        Returns:
            Single result row as dict, or None if no results

        Raises:
            asyncpg.PostgresError: If query fails
        """
        pool = cls.get_pool()
        async with pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    @classmethod
    async def execute_scalar(cls, query: str, *args) -> Optional[any]:
        """Execute a query and return a single scalar value.

        Args:
            query: SQL query string
            *args: Query parameters

        Returns:
            Single scalar value, or None if no results

        Raises:
            asyncpg.PostgresError: If query fails
        """
        pool = cls.get_pool()
        async with pool.acquire() as connection:
            return await connection.fetchval(query, *args)

    @classmethod
    async def execute_update(
        cls, query: str, *args
    ) -> int:
        """Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query string
            *args: Query parameters

        Returns:
            Number of affected rows

        Raises:
            asyncpg.PostgresError: If query fails
        """
        pool = cls.get_pool()
        async with pool.acquire() as connection:
            return await connection.execute(query, *args)


# Helper function for convenience
async def get_db_pool() -> asyncpg.Pool:
    """Get the database connection pool.

    Returns:
        The asyncpg connection pool

    Raises:
        RuntimeError: If pool has not been initialized
    """
    return DatabasePool.get_pool()
