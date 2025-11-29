from datetime import datetime
from app.db.connection import get_session_cm
from app.models.message import Message
from app.repository.device_state import DeviceStateRepository


class DeviceStateService:

    async def add_from_message(self, message: Message):
        async with get_session_cm() as session:
            await DeviceStateRepository(session).add_from_message(message)
