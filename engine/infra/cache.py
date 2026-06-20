import redis.asyncio as redis
from engine.core.settings import settings

class Cache:
    def __init__(self):
        self.redis = redis.from_url(settings.redis_url, decode_responses=True)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def set(self, key: str, value: str, ex: int = None):
        await self.redis.set(key, value, ex=ex)

    async def delete(self, key: str):
        await self.redis.delete(key)

cache_client = Cache()
