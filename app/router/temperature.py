from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter
from app.repository.temperature import TemperatureRepository
from app.models.measurement import ReadData, AggregationData
from app.utils.fill_default_date_range import fill_default_date_range

router = APIRouter(prefix="/temperature", tags=["temperature"])


@router.get("", response_model=ReadData)
async def get_temperature(
    repository: TemperatureRepository,
    device_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    start_date, end_date = fill_default_date_range(start_date, end_date)
    chart_data = await repository.get_sensor_temperatures(
        device_id, start_date, end_date
    )
    aggregation_data = await repository.get_aggregation_data(
        device_id, start_date, end_date
    )
    return ReadData(
        chart_data=chart_data, aggregation_data=AggregationData(**aggregation_data)
    )
