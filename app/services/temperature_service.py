from datetime import datetime
from app.db.connection import get_session
from app.models.measurement import TemperatureMeasurement
from app.models.message import Message


class TemperatureService:

    async def add_from_message(self, message: Message):
        async with get_session() as session:
            timestamp = datetime.now()
            if timestamp.minute > 30:
                timestamp = timestamp.replace(hour=timestamp.hour + 1)
            timestamp = timestamp.replace(minute=0)
            measurement = TemperatureMeasurement(
                sensor_id=message.device_id,
                temperature=message.payload["temperature"],
                timestamp=timestamp,
            )
            session.add(measurement)
            await session.commit()
