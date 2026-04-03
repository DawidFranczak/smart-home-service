from sqlalchemy.sql.annotation import Annotated

from app.db.connection import SessionDB
from app.models.device_event import DeviceEvent
from fastapi import Depends


class DeviceEventRepository:
    def __init__(self, session: SessionDB):
        self.session = session

    async def add(self, event: DeviceEvent):
        self.session.add(event)
        await self.session.commit()


DeviceEventRepoDep = Annotated[DeviceEventRepository, Depends(DeviceEventRepository)]
