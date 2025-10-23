from typing import Optional
from datetime import datetime
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel, Field


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


class TemperatureMeasurement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    value: float
    sensor_id: str
    timestamp: datetime


class HumidityMeasurement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    value: float
    sensor_id: str
    timestamp: datetime
