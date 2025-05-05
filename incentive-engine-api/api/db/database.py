# incentive-engine-api/api/db/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api.config import DATABASE_URL
from api.db.models import Base

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,       # Log SQL for debugging; set to False in production
    future=True
)

# Session factory for AsyncSession
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """
    Initialize the database by creating all tables.
    Should be called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
