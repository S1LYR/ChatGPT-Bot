import func
import markups as mk
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


btnClear = KeyboardButton("Очистить контекст")
btnStyleMenu = KeyboardButton("Изменить стиль")
btnSub = KeyboardButton("Моя подписка")
btnHelp = KeyboardButton("Помощь")
btnLanguage = KeyboardButton("Выбрать язык")

lanMenu=InlineKeyboardMarkup(row_width=2)
btnRU = InlineKeyboardButton(text="Русский", callback_data="RU")
btnEN = InlineKeyboardButton(text="English", callback_data="EN")
lanMenu.add(btnRU, btnEN)

styleMenu  = InlineKeyboardMarkup(row_width=2)
btn_Mary  = InlineKeyboardButton(text="Выбрать Мэри", callback_data="Mary")
btn_Clover = InlineKeyboardButton(text="Выбрать Кловер", callback_data="Clover")
btn_Nat_Chan = InlineKeyboardButton(text="Выбрать Нат-Чан", callback_data="Nat-Chan")
btn_Max = InlineKeyboardButton(text="Выбрать Макс", callback_data="Max")
styleMenu.add(btn_Mary, btn_Clover, btn_Nat_Chan, btn_Max)

btnTopUP = InlineKeyboardButton(text="Оформить подписку?", callback_data="/pay")
topUpMenu = InlineKeyboardMarkup(row_width=1)
topUpMenu.insert(btnTopUP)
MainMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(btnClear, btnHelp, btnSub, btnLanguage, btnStyleMenu)

def buy_menu(isUrl=True, url="", bill=""):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI = InlineKeyboardButton(text="Ссылка на оплату", url=url)
        qiwiMenu.insert(btnUrlQIWI)

    btncheckQIWI = InlineKeyboardButton(text= "Проверить оплату", callback_data="check_"+bill)
    qiwiMenu.insert(btncheckQIWI)
    return qiwiMenu