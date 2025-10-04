import aio_pika
from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI

from app.db.connection import create_db_tables
from app.settings.rebbitmq_settings import RabbitMQSettings


@asynccontextmanager
async def startup_event(app: FastAPI):
    await create_db_tables()
    asyncio.create_task(consume())
    yield

async def consume():
    settings = RabbitMQSettings()
    amqp_url = settings.amqp_url
    queue_name = settings.QUEUE_NAME
    while True:
        try:
            connection = await aio_pika.connect_robust(amqp_url)
            break
        except Exception as e:
            print(f"RabbitMQ not ready, retrying in 5s... ({e})")
            await asyncio.sleep(5)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(f"Received from {queue_name}: {message.body.decode()}")
