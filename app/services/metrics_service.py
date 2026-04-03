from app.db.connection import SessionDB
import json
from datetime import datetime

from app.models.measurement import Measurement
from app.repository.measurement_repository import MeasurementRepository


class MetricsService:
    def __init__(self, session: SessionDB):
        self.session = session
        self.repository = MeasurementRepository(session=session)

    async def process_from_rabbit(self, body: bytes):
        full_message = json.loads(body)
        args, kwargs, embed = full_message
        event_data = args[0]
        raw_timestamp = event_data["timestamp"]["__value__"]
        event = Measurement(
            event=event_data["message_event"],
            device_id=event_data["device_id"],
            peripheral_id=event_data["peripheral_id"],
            home_id=event_data["home_id"],
            value=event_data["payload"]["value"],
            timestamp=datetime.fromisoformat(raw_timestamp),
        )
        await self.repository.add(event)
