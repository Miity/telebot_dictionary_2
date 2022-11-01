from aiogram.dispatcher.filters.state import StatesGroup, State


class Create_states(StatesGroup):
    start = State()
    level_1 = State()
    level_2 = State()
    level_3 = State()

class Create_dictionary(StatesGroup):
    title = State()
    source_lang = State()
    dist = State()

class In_dictionary(StatesGroup):
    start = State()
    edit_translate = State()
    edit_dict = State()
