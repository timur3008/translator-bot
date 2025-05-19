from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from googletrans import Translator

from keyboards.inline import languages_kb, translations_kb
from keyboards.reply import start_kb
from misc.state import TranslationState
from database.main import translations_repo, users_repo

router = Router()
translator = Translator()

@router.callback_query(F.data.startswith('next_page'))
async def next_languages(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    print(state_data)
    data = call.data
    _, start, limit, page, total_pages = data.split(':')

    if int(page) == int(total_pages):
        return await call.answer(text='Последняя страница', show_alert=True)

    await call.message.edit_reply_markup(
        reply_markup=languages_kb(
            start=int(start) + 9,
            limit=int(limit) + 9,
            current_page=int(page) + 1,
            is_from=state_data.get('is_from')
        )
    )

@router.callback_query(F.data.startswith('prev_page'))
async def prev_languages(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    data = call.data
    _, start, limit, page = data.split(':')

    if int(page) == 1:
        return await call.answer(text='Первая страница', show_alert=True)

    await call.message.edit_reply_markup(
        reply_markup=languages_kb(
            start=int(start) - 9,
            limit=int(limit) - 9,
            current_page=int(page) - 1,
            is_from=state_data.get('is_from')
        )
    )

@router.callback_query(F.data.startswith('get_lang_from'))
async def get_lang_from(call: CallbackQuery, state: FSMContext):
    await call.answer()

    _, lang_code = call.data.split(':')

    await state.update_data(is_from=False, lang_from=lang_code)
    # await state.set_state(TranslationState.lang_to)

    await call.message.edit_text(
        text='<b>Выберите язык, на который хотите сделать перевод</b>',
        reply_markup=languages_kb(is_from=False),
        parse_mode='HTML'
    )

@router.callback_query(F.data.startswith('get_lang_to'))
async def get_lang_to(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    print(state_data)
    _, lang_code = call.data.split(':')

    await call.message.answer(
        text='Напишите текст для перевода',
        reply_markup=None
    )
    await state.update_data(lang_to=lang_code)
    await state.set_state(TranslationState.text)

from datetime import datetime

@router.message(TranslationState.text)
async def translate(message: Message, state: FSMContext):
    state_data = await state.get_data()

    lang_from = state_data.get('lang_from')
    lang_to = state_data.get('lang_to')
    text = message.text
    translated_text = translator.translate(text=text, dest=lang_to, src=lang_from).text

    user_id = users_repo.get_user(chat_id=message.from_user.id)
    translations_repo.add_translation(
        lang_from=lang_from,
        lang_to=lang_to,
        original=text,
        translated=translated_text,
        created_at=datetime.now(),
        user_id=user_id[0]
    )

    await message.answer(
        text=f'<b>FROM</b>: {lang_from}\n<b>TO</b>: {lang_to}\n<b>ORIGINAL</b>: {text}\n<b>TRANSLATION</b>: {translated_text}',
        reply_markup=start_kb(),
        parse_mode='HTML'
    )
    await state.clear()

@router.callback_query(F.data.startswith('prev_translation'))
async def prev_translation(call: CallbackQuery):
    _, index, chat_id, page = call.data.split(':')

    if int(page) == 1:
        return call.answer(
            text='Первая страница переводов',
            show_alert=True
        )
    
    data, translation_button = translations_kb(
        index=int(index) - 1,
        current_page=int(index) - 1,
        user_id=chat_id
    )
    id, lang_from, lang_to, original, translated, created_at, user_id = data
    
    await call.message.edit_text(
        text=f'<b>FROM</b>: {lang_from}\n<b>TO</b>: {lang_to}\n<b>ORIGINAL</b>: {original}\n<b>TRANSLATION</b>: {translated}\n<b>DATE</b>: {created_at[:19]}',
        parse_mode='HTML'
    )
    await call.message.edit_reply_markup(
        reply_markup=translation_button
    )

@router.callback_query(F.data.startswith('next_translation'))
async def next_translation(call: CallbackQuery):
    _, index, chat_id, page, total_pages = call.data.split(':')

    if int(page) == int(total_pages):
        return call.answer(
            text='Последняя страница переводов',
            show_alert=True
        )
    
    data, translation_button = translations_kb(
        index=int(index) + 1,
        current_page=int(page) + 1,
        user_id=chat_id
    )
    id, lang_from, lang_to, original, translated, created_at, user_id = data
    
    await call.message.edit_text(
        text=f'<b>FROM</b>: {lang_from}\n<b>TO</b>: {lang_to}\n<b>ORIGINAL</b>: {original}\n<b>TRANSLATION</b>: {translated}\n<b>DATE</b>: {created_at[:19]}',
        parse_mode='HTML'
    )
    await call.message.edit_reply_markup(
        reply_markup=translation_button
    )