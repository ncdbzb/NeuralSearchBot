from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON


router = Router()


@router.message()
async def error_message(message: Message):
    await message.reply(text=LEXICON['no_echo'])
