from aiogram.fsm.state import State, StatesGroup

class TranslationState(StatesGroup):
    lang_to = State()
    text = State()