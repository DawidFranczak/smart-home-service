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
        data = json.loads(body)
        event = Measurement(
            message_id=data["message_id"],
            event=data["message_event"],
            device_id=data["device_id"],
            peripheral_id=data["peripheral_id"],
            home_id=data["home_id"],
            value=data["payload"]["value"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
        await self.repository.add(event)
