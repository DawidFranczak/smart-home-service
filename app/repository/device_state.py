from app.db.connection import SessionDB
from app.models.message import Message
from app.models.device_state import DeviceState
from datetime import datetime


class DeviceStateRepository:
    def __init__(self, session: SessionDB):
        self.session = session

    async def add_from_message(self, message: Message):
        state = DeviceState(
            timestamp=datetime.now(),
            device_id=message.device_id,
            value=message.payload["state"],
        )
        self.session.add(state)
        await self.session.commit()
