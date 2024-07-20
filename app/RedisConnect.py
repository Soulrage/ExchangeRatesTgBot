import asyncio
from datetime import datetime
import redis
from .ParsingCurrentRate import parsing_current_rate


class Redis:
    def __init__(self):
        self.r = redis.Redis(host='redis', port=6379)
        self.date = None

    async def update_rate(self):
        rate = await parsing_current_rate()
        for key in rate:
            self.r.set(key, rate[key])

    def get_rate(self, name_key: str):
        return self.r.get(name_key)

    def get_all_rate(self):
        all_rate = {}
        for rate in self.r.keys('*'):
            key = rate.decode('utf-8')
            value = self.r.get(key).decode('utf-8')
            all_rate[key] = value
        return all_rate
