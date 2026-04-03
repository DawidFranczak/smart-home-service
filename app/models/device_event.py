from datetime import datetime
from typing import Any, Optional

from sqlalchemy import JSON, Index, Column, DateTime
from sqlmodel import SQLModel, Field


class DeviceEvent(SQLModel, table=True):
    __tablename__ = "device_event"
    __table_args__ = (
        Index("ix_device_event_device_id", "device_id", "peripheral_id", "timestamp"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    event: str
    device_id: str
    peripheral_id: int
    home_id: int
    payload: dict[str, Any] = Field(default_factory=dict, sa_type=JSON)
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), index=True))
