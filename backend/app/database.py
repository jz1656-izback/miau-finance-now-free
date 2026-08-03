from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# 🔒 Database connection pooling configuration
# Uses NullPool for tests since they don't need connection persistence

engine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.environment == "development",
    connect_args={"timeout": 10, "ssl": False},
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
