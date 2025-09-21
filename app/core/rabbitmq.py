import aio_pika

class RabbitMQClient:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def publish(self, queue_name: str, message: str):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue_name
        )