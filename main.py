import asyncio
from aiogram import Bot, Dispatcher
from app.RedisConnect import Redis
from app.handlers import router


async def main():
    bot = Bot(token='token')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    redis = Redis()
    await redis.scheduled_update()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
