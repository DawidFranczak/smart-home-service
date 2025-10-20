from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlalchemy import func
from sqlmodel import select
from app.db.connection import SessionDB
from app.models.measurement import TemperatureMeasurement
from app.models.message import Message


class TemperatureRepository:
    def __init__(self, session: SessionDB):
        self.session = session

    async def get_sensor_temperatures(
        self, sensor_id: str, start_date: datetime, end_date: datetime
    ):
        result = await self.session.execute(
            select(
                TemperatureMeasurement.timestamp, TemperatureMeasurement.value
            ).where(
                TemperatureMeasurement.sensor_id == sensor_id,
                TemperatureMeasurement.timestamp >= start_date,
                TemperatureMeasurement.timestamp < end_date,
            )
        )
        return result.mappings()

    async def get_aggregation_data(
        self, sensor_id: str, start_date: datetime, end_date: datetime
    ) -> dict:
        value = await self.session.execute(
            select(
                func.avg(TemperatureMeasurement.value),
                func.max(TemperatureMeasurement.value),
                func.min(TemperatureMeasurement.value),
            ).where(
                TemperatureMeasurement.sensor_id == sensor_id,
                TemperatureMeasurement.timestamp >= start_date,
                TemperatureMeasurement.timestamp <= end_date,
            )
        )
        return value.mappings().all()[0]

    async def exists_by_timestamp_and_sensor_id(
        self, sensor_id: str, timestamp: datetime
    ) -> bool:
        result = await self.session.execute(
            select(TemperatureMeasurement).where(
                TemperatureMeasurement.sensor_id == sensor_id,
                TemperatureMeasurement.timestamp == timestamp,
            )
        )
        if result.scalars().first():
            return True
        return False

    async def add_from_message(self, message: Message, timestamp: datetime):
        measurement = TemperatureMeasurement(
            sensor_id=message.device_id,
            value=message.payload["temperature"],
            timestamp=timestamp,
        )
        self.session.add(measurement)
        await self.session.commit()


TemperatureRepository = Annotated[TemperatureRepository, Depends(TemperatureRepository)]
