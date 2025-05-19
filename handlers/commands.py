from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart

from keyboards.reply import start_kb
from database.main import users_repo

# История, Перевод
router = Router()

@router.message(CommandStart())
async def start(message: Message):
    chat_id = message.from_user.id
    users_repo.add_user(chat_id=chat_id)
    await message.answer(
        '<b>Вас приветствует бот-переводчик.\nВыберите действие ниже</b>',
        reply_markup=start_kb(),
        parse_mode='HTML'
    )