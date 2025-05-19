from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import languages_kb, translations_kb
from keyboards.reply import start_kb
from database.main import translations_repo

router = Router()

@router.message(F.text == 'Перевод')
async def handle_translate(message: Message, state: FSMContext):
    await message.answer(
        '<b>Выберите язык, с которого хотите перевести</b>',
        reply_markup=languages_kb(),
        parse_mode='HTML'
    )
    await state.update_data(is_from=True)

@router.message(F.text == 'История')
async def handle_translate(message: Message):
    await message.answer('Ваша история переводов')
    data, translations_button = translations_kb(user_id=message.from_user.id)
    if translations_button is None:
        return await message.answer(
            text=data,
            reply_markup=start_kb(),
            parse_mode='HTML'
        )
    _, lang_from, lang_to, original, translated, created_at, user_id = data

    data = translations_repo.get_translations(chat_id=message.from_user.id)
    await message.answer(
        text=f'<b>FROM</b>: {lang_from}\n<b>TO</b>: {lang_to}\n<b>ORIGINAL</b>: {original}\n<b>TRANSLATION</b>: {translated}\n<b>DATE</b>: {created_at[:19]}',
        parse_mode='HTML',
        reply_markup=translations_button
    )