import logging
import asyncio
from typing import Type

import aiormq
from aiormq.abc import DeliveredMessage
from app.db.connection import get_session_cm
from app.services.protocol import RabbitProcessor
from app.settings.rebbitmq_settings import RabbitMQSettings

logger = logging.getLogger(__name__)


async def consume_queue(
    exchange: str, queue_name: str, service_cls: Type[RabbitProcessor]
):
    settings = RabbitMQSettings()
    connection = await aiormq.connect(settings.amqp_url)
    channel = await connection.channel()
    await channel.queue_declare(queue_name, durable=True)
    await channel.exchange_declare(exchange, exchange_type="topic")
    await channel.queue_bind(queue_name, exchange, f"sensor_service.{queue_name}")
    await channel.queue_bind(queue_name, exchange, f"sensor_service.{queue_name}.*")

    async def on_message(message: DeliveredMessage):
        print(message.body)
        delivery_tag = message.delivery.delivery_tag
        try:
            async with get_session_cm() as session:
                service_instance = service_cls(session=session)
                await service_instance.process_from_rabbit(message.body)
            await message.channel.basic_ack(delivery_tag)
        except Exception as e:
            logger.error(f"Error processing message from {queue_name}: {e}")
            await message.channel.basic_nack(delivery_tag, requeue=True)

    await channel.basic_consume(queue_name, on_message)
    logger.debug(f"Started consuming {queue_name}")
    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.info(f"Stopping consumer for {queue_name}...")
    finally:
        await connection.close()
        logger.debug(f"Connection for {queue_name} closed.")
