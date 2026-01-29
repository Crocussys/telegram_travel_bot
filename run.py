import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, LabeledPrice, PreCheckoutQuery

from src import fileids, keyboard, receipt

TOKEN = getenv("BOT_TOKEN")
PROVIDER_TOKEN = getenv("BOT_PROVIDER_TOKEN")
WORK_DIR = getenv("WORK_DIR")
CONF_DIR = f"{WORK_DIR}/src/conf"

dp = Dispatcher()
files = fileids.Files(f"{CONF_DIR}/fileids.json")
kb = keyboard.Keyboard()
rcept_f = receipt.ReceiptFactory(
    f"{CONF_DIR}/products.json",
    f"{CONF_DIR}/customer.json"
)


@dp.message(CommandStart())
@dp.message(F.text == "Выбрать другой гайд")
async def command_start_handler(message: Message) -> None:
    kb.set([
        [
            KeyboardButton(text="Нижний Новгород"),
            KeyboardButton(text="Санкт-Петербург")
        ],
    ])

    await message.answer_photo(photo=files.photo("menu"), caption="Выберите интересующий вас гайд", reply_markup=kb.get())

@dp.message(F.text == "Нижний Новгород")
async def nn(message: Message) -> None:
    kb.set([
        [
            KeyboardButton(text="Кафе Нижнего"),
        ],
        [
            KeyboardButton(text="Выбрать другой гайд"),
        ]
    ])
    await message.answer("Выберите интересующий вас гайд", reply_markup=kb.get())

@dp.message(F.text == "Кафе Нижнего")
async def cafes_nn(message: Message) -> None:
    kb.set([
        [KeyboardButton(text="Обновление гайда"), KeyboardButton(text="Выбрать другой гайд")]
    ])
    rcept = rcept_f.get_receipt("cafes_nn")
    
    await message.answer_photo(photo=files.photo("cafes_nn"))
    with open(f"{WORK_DIR}/texts/cafes_nn1.html", "rb") as text_file:
        await message.answer(text_file.read(), reply_markup=kb.get())
    await message.answer_invoice(
        rcept.get_name(),
        rcept.get_description(),
        message.date.strftime(f"0-{message.from_user.id}-%d.%m.%Y-%H:%M:%S"),
        rcept.get_currency(),
        [LabeledPrice(label=rcept.get_name(), amount=int(float(rcept.get_amount()) * 100))],
        PROVIDER_TOKEN,
        need_phone_number=True,
        need_email=True,
        send_phone_number_to_provider=True,
        send_email_to_provider=True,
        provider_data=rcept.get_provider_data()
    )

@dp.message(F.text == "Санкт-Петербург")
async def spb(message: Message) -> None:
    kb.set([
        [
            KeyboardButton(text="Апартаменты и отели"),
        ],
        [
            KeyboardButton(text="Выбрать другой гайд"),
        ]
    ])
    await message.answer("Выберите интересующий вас гайд", reply_markup=kb.get())

@dp.message(F.text == "Апартаменты и отели")
async def hotels_spb(message: Message) -> None:
    kb.set([
        [KeyboardButton(text="Обновление гайда"), KeyboardButton(text="Выбрать другой гайд")]
    ])
    rcept = rcept_f.get_receipt("hotels_spb")
    
    await message.answer_photo(photo=files.photo("hotels_spb"))
    with open(f"{WORK_DIR}/texts/hotels_spb1.html", "rb") as text_file:
        await message.answer(text_file.read(), reply_markup=kb.get())
    await message.answer_invoice(
        rcept.get_name(),
        rcept.get_description(),
        message.date.strftime(f"1-{message.from_user.id}-%d.%m.%Y-%H:%M:%S"),
        rcept.get_currency(),
        [LabeledPrice(label=rcept.get_name(), amount=int(float(rcept.get_amount()) * 100))],
        PROVIDER_TOKEN,
        need_phone_number=True,
        need_email=True,
        send_phone_number_to_provider=True,
        send_email_to_provider=True,
        provider_data=rcept.get_provider_data()
    )

@dp.message(F.text == "Обновление гайда")
async def another_guide(message: Message) -> None:
    with open(f"{WORK_DIR}/texts/update_guide.html", "rb") as text_file:
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
    with open(f"{WORK_DIR}/texts/successful_payment.html", "rb") as text_file:
        await message.answer(text_file.read())
    invoice = message.successful_payment.invoice_payload.split("-")
    product_id = int(invoice[0])
    if product_id == 0:
        await message.answer_document(files.doc("cafes_nn"), protect_content=True)
    elif product_id == 1:
        await message.answer_document(files.doc("hotels_spb"), protect_content=True)

@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Пожалуйста пользуйтесь кнопками", reply_markup=kb.get())

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
