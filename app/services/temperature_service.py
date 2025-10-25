from datetime import datetime

from app.db.connection import get_session_cm
from app.models.message import Message
from app.repository.temperature import TemperatureRepository


class TemperatureService:

    async def add_from_message(self, message: Message):
        async with get_session_cm() as session:
            timestamp = datetime.fromisoformat(message.payload["timestamp"])
            if await TemperatureRepository(session).exists_by_timestamp_and_sensor_id(
                message.device_id, timestamp
            ):
                return
            await TemperatureRepository(session).add_from_message(message, timestamp)
