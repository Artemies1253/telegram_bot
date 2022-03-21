from aiogram import types
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async
from django.conf import settings

from src.telegram_bot.enums import SoftwareSection
from src.telegram_bot.models import ProblemStatement, Photo
from src.telegram_bot.states import ProblemStatementGroup
from src.telegram_bot.services import BOT


async def start_problem_statement_group(message: types.Message):
    """Start point ProblemStatementGroup"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    markup.add(SoftwareSection.RMK.value, SoftwareSection.RMD.value)
    markup.add(SoftwareSection.terminal.value, SoftwareSection.exploitation.value)
    markup.add(SoftwareSection.timetable.value, SoftwareSection.reports.value)

    await ProblemStatementGroup.start.set()

    await message.answer(
        "Здравствуйте. Это техподдержка. Выберите раздел ПО, где возникла проблема",
        reply_markup=markup
    )


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


async def process_start_invalid(message: types.Message):
    return await message.reply("Выберете раздел По из предложенных вариантов")


async def process_answer_first_name_and_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['software_section'] = message.text

    await ProblemStatementGroup.next()

    await message.answer("Ваши фамилия и имя", reply_markup=types.ReplyKeyboardRemove())


async def process_answer_first_name_and_last_name_invalid(message: types.Message):
    return await message.reply("Имя и фамилия должны быть разделены пробелом и состоять только из букв")


async def process_answer_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text

    await ProblemStatementGroup.next()

    await message.answer("Ваша должность")


async def process_answer_position_invalid(message: types.Message):
    return await message.reply("Должность должна состоять только из букв, может содержать пробелы")


async def process_answer_description_of_problem(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['position'] = message.text

    await ProblemStatementGroup.next()

    await message.answer("Опишите проблему. При необходимости прикрепите фотографии")


async def process_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not data.get("description"):
            if message.text:
                data["description"] = message.text
            elif message.caption:
                data["description"] = message.caption

        if message.photo:
            photo_id = message.photo[0].file_id
            photos = data.get("photos")
            if photos:
                photos.append(photo_id)
            else:
                data["photos"] = [photo_id]

    if message.text or message.caption:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add("Отправить обращение", "Отмена")
        await message.answer(
            "Если вы предоставили всю необходимую информацию, нажмите отправить обращение,"
            "для отмены нажмите кнопку отмены",
            reply_markup=markup
        )


async def save_data_and_send_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        full_name = data.get('full_name')
        software_section = data.get('software_section')
        position = data.get('position')
        description = data.get("description")
        photos = data.get("photos")
        problem_statement = await sync_to_async(ProblemStatement.objects.create)(
            full_name=full_name,
            software_section=software_section,
            position=position,
            description=description,
        )
        if photos:
            for photo_id in photos:
                await sync_to_async(Photo.objects.create)(problem_statement=problem_statement,
                                                          instagram_file_id=photo_id)
    await message.answer(
        "Обращение принято. В ближайшее время с вами свяжется специалист поддержки",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot = BOT

    if photos:
        await bot.send_message(
            chat_id=settings.CHAT_ID_SUPPORT_SERVICE,
            text=f"Обращение о проблеме\n"
                 f"РАЗДЕЛ {problem_statement.software_section}\n"
                 f"ФИ {problem_statement.full_name}\n"
                 f"ОПИСАНИЕ {problem_statement.description}\n"
                 f"ФОТО"
        )
        for photo_id in photos:
            await bot.send_photo(
                chat_id=settings.CHAT_ID_SUPPORT_SERVICE,
                photo=photo_id)
    else:
        await bot.send_message(
            chat_id=settings.CHAT_ID_SUPPORT_SERVICE,
            text=f"Обращение о проблеме\n"
                 f"РАЗДЕЛ {problem_statement.software_section}\n"
                 f"ФИ {problem_statement.full_name}\n"
                 f"ОПИСАНИЕ {problem_statement.description}"
        )
    await state.finish()
