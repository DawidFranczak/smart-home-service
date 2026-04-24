import json
from datetime import datetime

from app.models.device_event import DeviceEvent
from app.db.connection import SessionDB
from app.repository.device_event_repository import DeviceEventRepository


class HistoryService:
    def __init__(self, session: SessionDB):
        self.session = session
        self.repository = DeviceEventRepository(session)

    async def process_from_rabbit(self, body: bytes) -> None:
        data = json.loads(body)
        event = DeviceEvent(
            message_id=data["message_id"],
            event=data["message_event"],
            device_id=data["device_id"],
            peripheral_id=data["peripheral_id"],
            home_id=data["home_id"],
            payload=data["payload"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )

        await self.repository.add(event)
