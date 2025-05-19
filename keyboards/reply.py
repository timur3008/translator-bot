from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_kb():
    kb = ReplyKeyboardBuilder()

    kb.button(text='Перевод')
    kb.button(text='История')

    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)