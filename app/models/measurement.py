from datetime import datetime

from sqlmodel import SQLModel, Field

class TemperatureMeasurement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    temperature: float
    sensor_id: str
    timestamp: datetime

class HumidityMeasurement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    humidity: float
    sensor_id: str
    timestamp: datetime