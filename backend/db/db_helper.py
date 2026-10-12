from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..core import settings
from ..models import Base


class DbHelper:
    def __init__(self, async_url: str, echo: bool = False):
        self.async_url = async_url
        self.echo = echo

        self.engine = create_async_engine(
            url=self.async_url,
            echo=self.echo,
        )

        self.session_local = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    async def get_db(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_local() as db:
            yield db

    async def create_tables(self):
        async with self.engine.begin as conn:
            await conn.run_sync(Base.metadata.create_all)


db_helper = DbHelper(
    async_url=settings.database_async_url,
    echo=True,
)
