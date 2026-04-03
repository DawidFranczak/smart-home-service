from fastapi import Depends
from sqlalchemy import select, func
from typing import Annotated

from app.db.connection import SessionDB
from app.models.measurement import Measurement
from app.schemas.measurement import MeasurementFilter


class MeasurementRepository:
    def __init__(self, session: SessionDB):
        self.session = session

    async def add(self, event: Measurement):
        self.session.add(event)
        await self.session.commit()

    async def get_raw_data(self, measurement_filter: MeasurementFilter):
        result = await self.session.execute(
            select(Measurement.timestamp, Measurement.value).where(
                Measurement.event == measurement_filter.event,
                Measurement.device_id == measurement_filter.device_id,
                Measurement.peripheral_id == measurement_filter.peripheral_id,
                Measurement.timestamp >= measurement_filter.start_date,
                Measurement.timestamp < measurement_filter.end_date,
            )
        )
        return result.mappings()

    async def get_aggregation_data(self, measurement_filter: MeasurementFilter) -> dict:
        value = await self.session.execute(
            select(
                func.avg(Measurement.value),
                func.max(Measurement.value),
                func.min(Measurement.value),
            ).where(
                Measurement.event == measurement_filter.event,
                Measurement.device_id == measurement_filter.device_id,
                Measurement.peripheral_id == measurement_filter.peripheral_id,
                Measurement.timestamp >= measurement_filter.start_date,
                Measurement.timestamp < measurement_filter.end_date,
            )
        )
        return value.mappings().all().first()


MeasurementRepoDep = Annotated[MeasurementRepository, Depends(MeasurementRepository)]
