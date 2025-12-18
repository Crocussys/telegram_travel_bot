from os import getenv
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import json


class Environments(dict):
    def __init__(self):
        super().__init__()

        self.update({
            "work_dir":      getenv("WORK_DIR"),
            "customer_file": getenv("CUSTOMER_FILE")
        })
        self.update({"conf_dir": f"{self["work_dir"]}/conf"})

        secrets_files = getenv("SECTRETS_ENV_FILES").split(";")
        for secret_file_path in secrets_files:
            self.update({data[:data.find("=")]: data[data.find("=") + 1:] for data in Path(secret_file_path).read_text().split("\n")})


class Files:
    def __init__(self, conf_file_path):
        with open(conf_file_path, "r") as conf_file:
            self.conf = json.loads(conf_file.read())
    
    def get(self):
        return self.conf
    
    def photo(self, name):
        return self.conf["photos"].get(name)
    
    def doc(self, name):
        return self.conf["documents"].get(name)


class ReceiptFactory:
    class Receipt:
        def __init__(self, conf, customer):
            self.conf = conf
            self.customer = customer
        
        def get_name(self):
            return self.conf["item"]["description"]
        
        def get_description(self):
            return self.conf["description"]
        
        def get_currency(self):
            return self.conf["item"]["amount"]["currency"]
        
        def get_amount(self):
            return self.conf["item"]["amount"]["value"]
        
        def get_provider_data(self):
            provider_data = {
                "receipt": {
                    "customer": self.customer,
                    "items": [self.conf["item"]]
                }
            }
            return json.dumps(provider_data)

    def __init__(self, conf_file_path, customer_file_path):
        with open(conf_file_path, "r") as conf_file:
            self.conf = json.loads(conf_file.read())
        with open(customer_file_path, "r") as file:
            self.customer = json.loads(file.read())

    def get_receipt(self, id):
        conf = self.conf.get(id)
        if conf is None:
            raise AttributeError
        return self.Receipt(conf, self.customer)


class Core:
    dp = Dispatcher()
    
    def __init__(self):
        self.env = Environments()
        self.files = Files(f"{self.env["conf_dir"]}/fileids.json")
        self.rcept_f = ReceiptFactory(
            f"{self.env["conf_dir"]}/products.json",
            self.env["customer_file"]
        )

    async def start_pooling(self):
        bot = Bot(token=self.env["bot_token"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await self.dp.start_polling(bot)

    @dp.message()
    async def message(self, message: Message) -> None:
        pass
