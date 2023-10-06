from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.settings import DATABASE_URL

async_engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session
