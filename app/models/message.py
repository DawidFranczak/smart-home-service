from pydantic import BaseModel

from app.enums.message_event import MessageEvent


class Message(BaseModel):
    message_event: MessageEvent
    device_id: int
    home_id: int
    payload: dict
