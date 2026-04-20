from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.db.connection import create_db_tables
from app.services.history_service import HistoryService
from app.services.metrics_service import MetricsService
from app.settings.rebbitmq_settings import RabbitMQSettings
from app.utils.consume_queue import consume_queue

running_tasks = []


@asynccontextmanager
async def startup_event(app: FastAPI):
    await create_db_tables()
    settings = RabbitMQSettings()
    task1 = asyncio.create_task(consume_queue(settings.EVENTS_QUEUE, HistoryService))
    task2 = asyncio.create_task(consume_queue(settings.METRICS_QUEUE, MetricsService))
    running_tasks.extend([task1, task2])

    try:
        yield
    finally:
        for task in running_tasks:
            task.cancel()
        await asyncio.gather(*running_tasks, return_exceptions=True)
