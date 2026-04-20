from typing import Protocol


class RabbitProcessor(Protocol):

    async def process_from_rabbit(self, body: bytes) -> None: ...
