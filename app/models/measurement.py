from datetime import datetime

from sqlmodel import SQLModel, Field

class TemperatureMeasurement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    temperature: float
    humidity: float
    sensor_id: int
    timestamp: datetime