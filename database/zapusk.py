import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from database.models import Base

zapusk = create_async_engine(os.getenv('DB_LITE'), echo=True)

session_maker = async_sessionmaker(bind=zapusk, class_=AsyncSession, expire_on_commit=False)


async def create_database():
    async with zapusk.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database():
    async with zapusk.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)