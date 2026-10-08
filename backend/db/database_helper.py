from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from collections.abc import AsyncGenerator
from ..core.config import settings
from ..models import Base


class DatabaseHelper:
    def __init__(self, database_url: str, echo: bool = False):
        self.database_url = database_url
        self.echo = echo

        self.async_engine = create_async_engine(
            url=self.database_url,
            echo=self.echo,
        )

        self.session_local = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def get_db(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_local() as db:
            yield db

    async def create_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db_helper = DatabaseHelper(
    database_url=settings.database_url,
    echo=True,
)
