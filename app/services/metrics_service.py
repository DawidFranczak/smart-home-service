class MetricsService:
    async def process_from_rabbit(self, data: bytes):
        print(data)
