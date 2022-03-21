from aiogram import Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from src.telegram_bot import validation
from src.telegram_bot.enums import SoftwareSection
from src.telegram_bot.states import ProblemStatementGroup
from src.telegram_bot.states_groups import problem_statement
from src.telegram_bot.services import cancel_handler, create_bot, BOT
from src.telegram_bot.validation import validate_position


class TelegramBot:
    def run(self):
        self.create_bot()
        self.register_states_group()
        self.run_bot()

    def create_bot(self):
        self.bot = BOT
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)

    def register_states_group(self):
        self.register_problem_statement()

    def register_problem_statement(self):
        self.dp.register_message_handler(
            problem_statement.start_problem_statement_group,
            commands=["start", "help", "старт"], state=None
        )
        self.dp.register_message_handler(cancel_handler, state="*", commands=['cancel', "отмена"])
        self.dp.register_message_handler(
            cancel_handler,
            Text(equals=['cancel', 'отмена'], ignore_case=True), state='*'
        )
        self.dp.register_message_handler(
            problem_statement.process_start_invalid,
            lambda message: message.text not in SoftwareSection.get_list_value(),
            state=ProblemStatementGroup.start
        )
        self.dp.register_message_handler(
            problem_statement.process_answer_first_name_and_last_name,
            state=ProblemStatementGroup.start
        )
        self.dp.register_message_handler(
            problem_statement.process_answer_first_name_and_last_name_invalid,
            lambda message: not validation.validate_first_name_and_last_name(message.text),
            state=ProblemStatementGroup.answer_first_name_and_last_name
        )
        self.dp.register_message_handler(
            problem_statement.process_answer_position,
            state=ProblemStatementGroup.answer_first_name_and_last_name
        )
        self.dp.register_message_handler(
            problem_statement.process_answer_position_invalid,
            lambda message: not validate_position(message.text),
            state=ProblemStatementGroup.answer_position
        )
        self.dp.register_message_handler(
            problem_statement.process_answer_description_of_problem,
            state=ProblemStatementGroup.answer_position
        )
        self.dp.register_message_handler(
            problem_statement.save_data_and_send_message,
            Text(equals=['Отправить обращение', 'Отмена'], ignore_case=True),
            state=ProblemStatementGroup.answer_description_of_problem,
        )
        self.dp.register_message_handler(
            problem_statement.process_finish,
            state=ProblemStatementGroup.answer_description_of_problem,
            content_types=["text", "photo"]
        )

    def run_bot(self):
        executor.start_polling(self.dp, skip_updates=True)
