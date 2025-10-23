from typing import Optional
from datetime import datetime

from fastapi import APIRouter

from app.models.measurement import ReadData, AggregationData
from app.repository.humidity import HumidityRepository
from app.utils.fill_default_date_range import fill_default_date_range

router = APIRouter(prefix="/humidity", tags=["humidity"])


@router.get("/", response_model=ReadData)
async def get_humidity(
    repository: HumidityRepository,
    device_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    start_date, end_date = fill_default_date_range(start_date, end_date)
    print(start_date, end_date)
    chart_data = await repository.get_sensor_humidities(device_id, start_date, end_date)
    aggregation_data = await repository.get_aggregation_data(
        device_id, start_date, end_date
    )
    return ReadData(
        chart_data=chart_data, aggregation_data=AggregationData(**aggregation_data)
    )
