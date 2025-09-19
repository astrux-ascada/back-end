import redis.asyncio as redis

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    async def publish(self, channel: str, message: str):
        await self.client.publish(channel, message)

    async def get(self, key: str):
        return await self.client.get(key)

    async def set(self, key: str, value: str, ex: int = None):
        await self.client.set(key, value, ex=ex)