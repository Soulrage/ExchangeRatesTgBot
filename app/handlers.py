from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!', reply_markup=kb.main)


@router.message(Command('exchange'))
async def cmd_exchange(message: Message):
    args = message.text.split()
    if len(args) == 4:
        base_currency = args[0]  # USD
        target_currency = args[1]  # RUB
        amount = args[2]
        print(base_currency, target_currency, amount)
    else:
        await message.answer('Неверное количество аргументов. Используйте /exchange USD RUB 10')


@router.message(Command('rates'))
async def cmd_rates(message: Message):
    await message.answer(f'')