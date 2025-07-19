import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base


from app.api.utils.config import config as settings

logger = structlog.get_logger()

# Create async engine
engine = None
AsyncSessionLocal = None


async def init_db():
    """Initialize database connection"""
    global engine, AsyncSessionLocal

    try:
        # Convert sync URL to async URL
        async_database_url = settings.DATABASE_URL.replace(
            "postgresql://", "postgresql+asyncpg://"
        )

        # Create async engine
        engine = create_async_engine(
            async_database_url,
            echo=settings.DEBUG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_timeout=settings.DB_POOL_TIMEOUT,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

        # Create session factory
        AsyncSessionLocal = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        # Test connection
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute(text("SELECT 1")))

        logger.info("Database connection established successfully")

    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


async def close_db():
    """Close database connection"""
    global engine

    if engine:
        await engine.dispose()
        logger.info("Database connection closed")


async def get_db() -> AsyncSession:
    """Get database session"""
    if not AsyncSessionLocal:
        raise RuntimeError("Database not initialized")

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def health_check_db():
    """Health check for database"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda sync_conn: sync_conn.execute(text("SELECT 1")))
        return {
            "status": "healthy",
            "database": "postgresql",
            "timestamp": "2024-01-01T00:00:00Z",
        }
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "database": "postgresql",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z",
        }


# Create base class for models
Base = declarative_base()
