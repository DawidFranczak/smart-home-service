from pydantic import BaseModel, model_validator

from datetime import datetime

from app.models.user import UserModel
from app.utils.fill_default_date_range import fill_default_date_range


class MeasurementFilter(BaseModel):
    peripheral_id: int
    event: str
    start_date: datetime
    end_date: datetime
    user: UserModel

    @model_validator(mode="before")
    @classmethod
    def pre_fill_dates(cls, data: dict) -> dict:
        if isinstance(data, dict):
            start = data.get("start_date")
            end = data.get("end_date")

            new_start, new_end = fill_default_date_range(start, end)
            data["start_date"] = new_start
            data["end_date"] = new_end
        return data
