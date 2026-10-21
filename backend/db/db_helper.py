from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models import Base
from config import settings


class DatabaseHelper:
    def __init__(self, async_url: str, echo: bool = False):
        self.engine = create_async_engine(url=async_url, echo=echo)
        self.session_local = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_local() as db:
            yield db

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db_helper = DatabaseHelper(
    async_url=settings.database_async_url,
    echo=True,
)
