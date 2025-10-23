from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from app.settings.db_settings import DBSettings
from sqlalchemy import text

db_settings = DBSettings()

# Create the SQLAlchemy async engine
engine = create_async_engine(url=db_settings.db_url, echo=False)


async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Create the database tables
async def create_db_tables():
    """
    Asynchronously create all database tables defined in SQLModel metadata.
    """
    from app.models.measurement import TemperatureMeasurement, HumidityMeasurement

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session_cm() -> AsyncSession:
    """
    Async context manager that provides a new database session.

    Sets the PostgreSQL search_path to the configured schema before yielding the session.
    Intended for manual usage with `async with` in services or repositories.

    Example:
        async with get_session_cm() as session:
            await SomeRepository(session).do_something()
    """
    async with async_session_maker() as session:
        await session.execute(
            text(f"SET search_path TO {db_settings.POSTGRES_SEARCH_PATH}")
        )
        yield session


async def get_session() -> AsyncSession:
    """
    Async generator that provides a database session for FastAPI dependencies.

    Sets the PostgreSQL search_path to the configured schema before yielding the session.
    Can be used with `Depends(get_session)` in FastAPI endpoints.

    Example:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_session)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with async_session_maker() as session:
        await session.execute(
            text(f"SET search_path TO {db_settings.POSTGRES_SEARCH_PATH}")
        )
        yield session


SessionDB = Annotated[AsyncSession, Depends(get_session)]
