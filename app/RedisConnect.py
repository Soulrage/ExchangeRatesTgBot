import asyncio
from datetime import datetime
import redis
from .ParsingCurrentRate import parsing_current_rate


class Redis:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379)
        self.date = None

    async def scheduled_update(self):
        await self.update_rate()
        while True:
            await asyncio.sleep(24 * 60 * 60)
            await self.update_rate()

    async def update_rate(self):
        rate = await parsing_current_rate()
        self.date = rate["date"]
        for key in rate:
            self.r.set(key, rate[key])

    def get_rate(self, name_key: str):
        print(datetime.now().strftime("%d.%m.%Y"))
        print(self.date)
        return self.r.get(name_key)

    def get_all_rate(self):
        all_rate = {}
        for rate in self.r.keys('*'):
            key = rate.decode('utf-8')
            value = self.r.get(key).decode('utf-8')
            all_rate[key] = value
        return all_rate
