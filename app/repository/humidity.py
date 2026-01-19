from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlmodel import select, func

from app.db.connection import SessionDB
from app.models.measurement import HumidityMeasurement
from app.models.message import Message


class HumidityRepository:
    def __init__(self, session: SessionDB):
        self.session = session

    async def get_sensor_humidities(
        self, sensor_id: int, start_date: datetime, end_date: datetime
    ):
        result = await self.session.execute(
            select(HumidityMeasurement.timestamp, HumidityMeasurement.value).where(
                HumidityMeasurement.sensor_id == sensor_id,
                HumidityMeasurement.timestamp >= start_date,
                HumidityMeasurement.timestamp < end_date,
            )
        )
        return result.mappings()

    async def get_aggregation_data(
        self, sensor_id: int, start_date: datetime, end_date: datetime
    ) -> dict:
        value = await self.session.execute(
            select(
                func.avg(HumidityMeasurement.value),
                func.max(HumidityMeasurement.value),
                func.min(HumidityMeasurement.value),
            ).where(
                HumidityMeasurement.sensor_id == sensor_id,
                HumidityMeasurement.timestamp >= start_date,
                HumidityMeasurement.timestamp <= end_date,
            )
        )
        return value.mappings().all()[0]

    async def exists_by_timestamp_and_sensor_id(
        self, sensor_id: int, timestamp: datetime
    ) -> bool:
        result = await self.session.execute(
            select(HumidityMeasurement).where(
                HumidityMeasurement.sensor_id == sensor_id,
                HumidityMeasurement.timestamp == timestamp,
            )
        )
        if result.scalars().first():
            return True
        return False

    async def add_from_message(self, message: Message, timestamp: datetime):
        measurement = HumidityMeasurement(
            sensor_id=message.device_id,
            value=message.payload["value"],
            timestamp=timestamp,
        )
        self.session.add(measurement)
        await self.session.commit()


HumidityRepository = Annotated[HumidityRepository, Depends(HumidityRepository)]
