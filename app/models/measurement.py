from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Index, Column, DateTime


class AggregationData(BaseModel):
    avg: Optional[float] = None
    max: Optional[float] = None
    min: Optional[float] = None


class ReadMeasurement(BaseModel):
    value: float
    timestamp: datetime


class ReadData(BaseModel):
    chart_data: list[ReadMeasurement]
    aggregation_data: AggregationData


class Measurement(SQLModel, table=True):
    __table_args__ = (
        Index(
            "ix_measurement_device_id",
            "peripheral_id",
            "event",
            "timestamp",
        ),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    event: str
    device_id: str
    peripheral_id: int
    home_id: int
    value: float
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), index=True))
