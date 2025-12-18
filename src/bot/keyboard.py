from aiogram.types import ReplyKeyboardMarkup


class Keyboard:
    def __init__(self):
        kb = []
        self.keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    def get(self):
        return self.keyboard
    
    def set(self, kb):
        self.keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
