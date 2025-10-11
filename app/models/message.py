from sqlmodel import SQLModel

from app.enums.message_event import MessageEvent
from app.enums.message_type import MessageType


class Message(SQLModel):
    message_type: MessageType
    message_event: MessageEvent
    device_id: str
    message_id: str
    payload: dict

