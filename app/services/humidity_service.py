from app.db.connection import get_session_cm
from app.models.message import Message
from app.repository.humidity import HumidityRepository
from app.utils.round_timestamp_to_nearest_hour import round_timestamp_to_nearest_hour


class HumidityService:

    async def add_from_message(self, message: Message):
        async with get_session_cm() as session:
            timestamp = round_timestamp_to_nearest_hour()
            if await HumidityRepository(session).exists_by_timestamp_and_sensor_id(
                message.device_id, timestamp
            ):
                return
            await HumidityRepository(session).add_from_message(message, timestamp)
