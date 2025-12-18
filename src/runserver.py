import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, LabeledPrice, PreCheckoutQuery

from bot.environments import Environments as env
from bot import fileids, keyboard, receipt

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
envs = env()
files = fileids.Files(f"{envs["conf_dir"]}/fileids.json")
kb = keyboard.Keyboard()
rcept_f = receipt.ReceiptFactory(
    f"{envs["conf_dir"]}/products.json",
    envs["customer_file"]
)


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
        [KeyboardButton(text="Кафе Нижнего")],
    ])

    await message.answer_photo(photo=files.photo("menu"), caption="Выберите интересующий вас гайд", reply_markup=kb.get())

@dp.message(F.text == "Кафе Нижнего")
async def cafes_nn(message: Message) -> None:
    kb.set([
        [KeyboardButton(text="Обновление гайда"), KeyboardButton(text="Выбрать другой гайд")]
    ])
    rcept = rcept_f.get_receipt("cafes_nn")
    
    await message.answer_photo(photo=files.photo("cafes_nn"))
    with open(f"{envs["work_dir"]}/texts/cafes_nn1.html", "rb") as text_file:
        await message.answer(text_file.read(), reply_markup=kb.get())
    await message.answer_invoice(
        rcept.get_name(),
        rcept.get_description(),
        message.date.strftime(f"{message.from_user.id}-%d.%m.%Y-%H:%M:%S"),
        rcept.get_currency(),
        [LabeledPrice(label=rcept.get_name(), amount=int(float(rcept.get_amount()) * 100))],
        envs["bot_provider_token"],
        need_phone_number=True,
        need_email=True,
        send_phone_number_to_provider=True,
        send_email_to_provider=True,
        provider_data=rcept.get_provider_data()
    )

@dp.message(F.text == "Обновление гайда")
async def another_guide(message: Message) -> None:
    with open(f"{envs["work_dir"]}/texts/update_guide.html", "rb") as text_file:
        await message.answer(text_file.read(), reply_markup=kb.get())

@dp.message(F.photo)
async def echo_handler(message: Message) -> None:
    print(f"File_id - {message.photo[0].file_id}")

@dp.message(F.document)
async def echo_handler(message: Message) -> None:
    print(f"File_id - {message.document.file_id}")

@dp.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    with open(f"{envs["work_dir"]}/texts/successful_payment.html", "rb") as text_file:
        await message.answer(text_file.read())
    await message.answer_document(files.doc("main_file"), protect_content=True)

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """

    await message.answer("Пожалуйста пользуйтесь кнопками", reply_markup=kb.get())

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=envs["bot_token"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
