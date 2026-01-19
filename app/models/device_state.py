from sqlmodel import SQLModel, Field
from datetime import datetime


class DeviceState(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime
    device_id: int
    home_id: int
    value: str
