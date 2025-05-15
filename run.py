import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

TOKEN = getenv("BOT_TOKEN")
WORK_DIR = getenv("WORK_DIR")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
@dp.message(F.text == "Выбрать другой гайд")
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`

    kb = [
        [KeyboardButton(text="Кафе Нижнего"), KeyboardButton(text="Обновление гайда")],
        # [KeyboardButton(text="Файл")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer_photo(photo="AgACAgIAAxkBAAMUaAYu_p_c5teyfdAQpdOQ-BPACmcAAirvMRtPQDFISX7aSKnEz_cBAAMCAANzAAM2BA",
                               caption="Выберете интересующий вас гайд", reply_markup=keyboard)
    # AgACAgIAAxkBAAMUaAYu_p_c5teyfdAQpdOQ-BPACmcAAirvMRtPQDFISX7aSKnEz_cBAAMCAANzAAM2BA

@dp.message(F.text == "Кафе Нижнего")
async def cafes_nn(message: Message) -> None:
    kb = [
        [KeyboardButton(text="Обновление гайда"), KeyboardButton(text="Выбрать другой гайд")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer_photo(photo="AgACAgIAAxkBAAMZaAYwL7Mfhhq18TnEzvF1c1emoXcAAj_vMRtPQDFIQ6TB-itBX8ABAAMCAANzAAM2BA")
    # AgACAgIAAxkBAAMZaAYwL7Mfhhq18TnEzvF1c1emoXcAAj_vMRtPQDFIQ6TB-itBX8ABAAMCAANzAAM2BA
    with open(f"{WORK_DIR}/texts/cafes_nn1.html", "rb") as text_file:
        await message.answer(text_file.read())
    with open(f"{WORK_DIR}/texts/cafes_nn2.html", "rb") as text_file:
        await message.answer(text_file.read(), reply_markup=keyboard)

@dp.message(F.text == "Обновление гайда")
async def another_guide(message: Message) -> None:
    await message.answer("Обновление гайда")

@dp.message(F.photo)
async def echo_handler(message: Message) -> None:
    print(f"File_id - {message.photo[0].file_id}")

@dp.message(F.document)
async def echo_handler(message: Message) -> None:
    print(f"File_id - {message.document.file_id}")

# @dp.message(F.text == "Файл")
# async def file(message: Message) -> None:
#     # BQACAgIAAxkBAAO_aCHBuribNkgjFkW9yl2tAu90HysAAltqAAIZhxFJYVFmrk4im_A2BA
#     await message.answer_document("BQACAgIAAxkBAAO_aCHBuribNkgjFkW9yl2tAu90HysAAltqAAIZhxFJYVFmrk4im_A2BA", protect_content=True)

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """

    await message.answer("Пожалуйста пользуйтесь кнопками")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
