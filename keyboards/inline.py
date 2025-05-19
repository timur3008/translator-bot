from typing import Any
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from googletrans import LANGUAGES

from database.main import translations_repo

def languages_kb(start: int = 0, limit: int = 9, current_page: int = 1, is_from=True):
    kb = InlineKeyboardBuilder()

    total_pages = round(len(LANGUAGES) / 9)
    

    for lang_code, lang_name in list(LANGUAGES.items())[start:limit]:
        if is_from:
            a = f'get_lang_from:{lang_code}'
        else:
            a = f'get_lang_to:{lang_code}'
        kb.button(text=lang_name.title(), callback_data=a)

    kb.adjust(3)

    kb.row(
        InlineKeyboardButton(text='<<<', callback_data=f'prev_page:{start}:{limit}:{current_page}'),
        InlineKeyboardButton(text=f'{current_page}:{total_pages}', callback_data='current'),
        InlineKeyboardButton(text='>>>', callback_data=f'next_page:{start}:{limit}:{current_page}:{total_pages}')
    )

    kb.row(
        InlineKeyboardButton(text='На главную', callback_data='home')
    )

    return kb.as_markup()

def translations_kb(index: int = 0, current_page: int = 1, user_id: int = None) -> tuple[Any, InlineKeyboardMarkup]:
    keyboard = InlineKeyboardBuilder()
    total_pages = len(translations_repo.get_translations(chat_id=user_id))

    if total_pages == 0:
        return '<b>❗️Вы ещё ничего не переводили❗️</b>', None

    data = translations_repo.get_translations(chat_id=user_id)[index]

    keyboard.row(
        InlineKeyboardButton(text='<<<', callback_data=f'prev_translation:{index}:{user_id}:{current_page}'),
        InlineKeyboardButton(text=f'{current_page}:{total_pages}', callback_data='current_page'),
        InlineKeyboardButton(text='>>>', callback_data=f'next_translation:{index}:{user_id}:{current_page}:{total_pages}')
    )
    return data, keyboard.as_markup()

