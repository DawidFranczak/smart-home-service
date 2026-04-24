from pydantic_settings import BaseSettings


class RabbitMQSettings(BaseSettings):
    RABBITMQ_FASTAPI_USER: str
    RABBITMQ_FASTAPI_PASSWORD: str
    RABBITMQ_ADDRESS: str
    NOTIFICATION_QUEUE: str
    EVENTS_QUEUE: str
    METRICS_QUEUE: str
    EXCHANGE: str

    @property
    def amqp_url(self) -> str:
        return f"amqp://{self.RABBITMQ_FASTAPI_USER}:{self.RABBITMQ_FASTAPI_PASSWORD}@{self.RABBITMQ_ADDRESS}/"
