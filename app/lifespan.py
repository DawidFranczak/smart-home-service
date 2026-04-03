from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.db.connection import create_db_tables
from app.services.history_service import HistoryService
from app.services.metrics_service import MetricsService
from app.settings.rebbitmq_settings import RabbitMQSettings
from app.utils.consume_queue import consume_queue


@asynccontextmanager
async def startup_event(app: FastAPI):
    await create_db_tables()
    settings = RabbitMQSettings()
    asyncio.create_task(consume_queue(settings.EVENTS_QUEUE, HistoryService))
    asyncio.create_task(consume_queue(settings.METRICS_QUEUE, MetricsService))
    yield
