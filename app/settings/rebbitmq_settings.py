from pydantic_settings import BaseSettings

class RabbitMQSettings(BaseSettings):
    RABBITMQ_FASTAPI_USER: str
    RABBITMQ_FASTAPI_PASSWORD: str
    RABBITMQ_ADDRESS: str
    QUEUE_NAME: str

    @property
    def amqp_url(self) -> str:
        return f"amqp://{self.RABBITMQ_FASTAPI_USER}:{self.RABBITMQ_FASTAPI_PASSWORD}@{self.RABBITMQ_ADDRESS}/"