from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.RedisConnect import Redis

router = Router()
redis = Redis()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('''/rates - узнать актуальный курс валют 
/exchange - AUD RUB 100 - узнать сколько рублей в 100 Австралийских долларах 
    ''')


@router.message(Command('exchange'))
async def cmd_exchange(message: Message):
    args = message.text.split()
    if len(args) == 4:
        target = args[1]  # USD
        base = args[2]  # RUB
        amount = args[3]
        print(target, base, amount)
        rate = redis.get_rate(target)
        try:
            decoded_rate = rate.decode('utf-8')
            result = float(decoded_rate.replace(',', '.')) * float(amount)
            await message.answer(str(result))
        except:
            await message.answer('Некорректные аргументы. Используйте /exchange USD RUB 10')
    else:
        await message.answer('Неверное количество аргументов. Используйте /exchange USD RUB 10')


@router.message(Command('rates'))
async def cmd_rates(message: Message):
    text = "Текущие курсы валют:\n"
    for currency, rate in redis.get_all_rate().items():
        text += f"{currency}: {rate}\n"

    await message.reply(text)