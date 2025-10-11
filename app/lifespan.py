import aio_pika
from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from app.db.connection import create_db_tables
from app.enums.message_event import MessageEvent
from app.models.message import Message
from app.services.humidity_service import HumidityService
from app.services.temperature_service import TemperatureService
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
    temperature_service = TemperatureService()
    humidity_service = HumidityService()

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
                    data = Message.model_validate_json(message.body.decode())
                    match data.message_event:
                        case MessageEvent.ON_MEASUREMENT_TEMP_HUM:
                            asyncio.create_task(
                                temperature_service.add_from_message(data)
                            )
                            asyncio.create_task(humidity_service.add_from_message(data))
