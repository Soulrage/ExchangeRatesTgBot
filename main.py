import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv
import os
from app.RedisConnect import Redis
from datetime import datetime, timedelta


async def main():
    load_dotenv()
    bot = Bot(token=f'{os.getenv("TOKEN")}')
    dp = Dispatcher()
    dp.include_router(router)

    asyncio.create_task(update_schedule())

    await dp.start_polling(bot)


async def update_schedule():
    redis = Redis()
    while True:
        await redis.update_rate()
        now = datetime.now()
        next_run = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_time = (next_run - now).total_seconds()

        await asyncio.sleep(wait_time)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
