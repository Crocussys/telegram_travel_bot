import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton

from src import fileids, keyboard

TOKEN = getenv("BOT_TOKEN")
WORK_DIR = getenv("WORK_DIR")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
files = fileids.Files(f"{WORK_DIR}/src/conf/fileids.json")
kb = keyboard.Keyboard()


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

    kb.set([
        [KeyboardButton(text="Кафе Нижнего"), KeyboardButton(text="Обновление гайда")],
        # [KeyboardButton(text="Файл")]
    ])

    await message.answer_photo(photo=files.photo("menu"), caption="Выберете интересующий вас гайд", reply_markup=kb.get())

@dp.message(F.text == "Кафе Нижнего")
async def cafes_nn(message: Message) -> None:
    kb.set([
        [KeyboardButton(text="Обновление гайда"), KeyboardButton(text="Выбрать другой гайд")]
    ])
    
    await message.answer_photo(photo=files.photo("cafes_nn"))
    with open(f"{WORK_DIR}/texts/cafes_nn1.html", "rb") as text_file:
        await message.answer(text_file.read())
    with open(f"{WORK_DIR}/texts/cafes_nn2.html", "rb") as text_file:
        await message.answer(text_file.read(), reply_markup=kb.get())

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

    await message.answer("Пожалуйста пользуйтесь кнопками", reply_markup=kb.get())


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
