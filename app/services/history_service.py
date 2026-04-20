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
        full_message = json.loads(body)
        args, kwargs, embed = full_message
        event_data = args[0]

        raw_timestamp = event_data["timestamp"]["__value__"]
        event = DeviceEvent(
            event=event_data["message_event"],
            device_id=event_data["device_id"],
            peripheral_id=event_data["peripheral_id"],
            home_id=event_data["home_id"],
            payload=event_data["payload"],
            timestamp=datetime.fromisoformat(raw_timestamp),
        )

        await self.repository.add(event)
