from aiogram import Bot, types
from aiogram.dispatcher import FSMContext

from django.conf import settings


BOT = Bot(token=settings.TOKEN_BOT)


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


def create_bot():
    return Bot(token=settings.TOKEN_BOT)
