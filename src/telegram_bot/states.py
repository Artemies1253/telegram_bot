from aiogram.dispatcher.filters.state import State, StatesGroup


class ProblemStatementGroup(StatesGroup):
    start = State()
    answer_first_name_and_last_name = State()
    answer_position = State()
    answer_description_of_problem = State()
