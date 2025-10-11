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
    from app.models.measurement import TemperatureMeasurement, HumidityMeasurement

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Get a new database session


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        await session.execute(
            text(f"SET search_path TO {db_settings.POSTGRES_SEARCH_PATH}")
        )
        yield session


SessionDB = Annotated[AsyncSession, Depends(get_session)]
