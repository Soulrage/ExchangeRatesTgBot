from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.RedisConnect import Redis

router = Router()
redis = Redis()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('''/rates - узнать актуальный курс валют 
/exchange AUD RUB 100 - узнать сколько рублей в 100 Австралийских долларах 
    ''')


@router.message(Command('help'))
async def start(message: Message):
    await message.answer('''/rates - узнать актуальный курс валют 
/exchange AUD RUB 100 - узнать сколько рублей в 100 Австралийских долларах 
    ''')


@router.message(Command('exchange'))
async def cmd_exchange(message: Message):
    args = message.text.split()
    if len(args) == 4:
        target = args[1]  # USD
        base = args[2]  # RUB
        amount = args[3]
        print(target, base, amount)
        rate_target = redis.get_rate(target)
        rate_base = redis.get_rate(base)
        try:
            decoded_rate_target = rate_target.decode('utf-8')
            decoded_rate_base = rate_base.decode('utf-8')
            result = float(decoded_rate_target.replace(',', '.')) / float(decoded_rate_base.replace(',', '.')) * float(amount)
            await message.answer(f"{amount} {target} = {str(result)} {base}.")
        except:
            await message.answer('Некорректные аргументы. Используйте /exchange USD RUB 10')
    else:
        await message.answer('Неверное количество аргументов. Используйте /exchange USD RUB 10')


@router.message(Command('rates'))
async def cmd_rates(message: Message):
    text = "Текущие курсы валют к рублю:\n\n"
    for currency, rate in redis.get_all_rate().items():
        text += f"{currency}: {rate}\n"
    await message.answer(text)


@router.message(F.text & ~F.command.commands)
async def handle_invalid_commands(message: Message):
    await message.answer("Извините, не могу обработать эту команду. Пожалуйста, воспользуйтесь доступными командами. Посмотреть доступные команды можно по комманде /start или /help")

