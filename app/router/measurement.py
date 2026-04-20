from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from app.auth.validate_user import User
from app.models.measurement import ReadData, AggregationData
from app.repository.measurement_repository import MeasurementRepoDep
from app.schemas.measurement import MeasurementFilter

router = APIRouter(prefix="/measurement", tags=["measurement"])


@router.get("", response_model=ReadData)
async def get_measurement(
    repository: MeasurementRepoDep,
    user: User,
    peripheral_id: int,
    event: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> ReadData:
    measurement_filter = MeasurementFilter(
        peripheral_id=peripheral_id,
        event=event,
        start_date=start_date,
        end_date=end_date,
        user=user,
    )
    chart_data = await repository.get_raw_data(measurement_filter)
    aggregation_data = await repository.get_aggregation_data(measurement_filter)
    return ReadData(
        chart_data=chart_data, aggregation_data=AggregationData(**aggregation_data)
    )
