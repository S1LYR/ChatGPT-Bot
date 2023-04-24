import logging
import openai
import sqlite3
import config
import time
import datetime
import func
import markups as mk
import random
from pyqiwip2p import QiwiP2P
from database import Database
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
def start_bot():
    logging.basicConfig(level=logging.INFO)
    p2p = QiwiP2P(auth_key=config.qiwi_token)
    db = Database("database.db")
    bot = Bot(token = config.TOKEN)
    dp = Dispatcher(bot)
    openai.api_key = config.api_key

    def lang_check(user_id, style):
        lan=db.get_language(user_id)
        if (lan == 1) and (style == 1):
            return config.ai_style_Mary_ru
        elif (lan == 1) and (style == 2):
            return config.ai_style_Clover_ru
        elif (lan == 1) and (style == 3):
            return config.ai_style_Nat_Chan_ru
        elif (lan == 1) and (style == 4):
            return config.ai_style_Max_ru
        elif (lan == 2) and (style == 1):
            return config.ai_style_Mary_en
        elif (lan == 2) and (style == 2):
            return config.ai_style_Clover_en
        elif (lan == 2) and (style == 3):
            return config.ai_style_Nat_Chan_en
        elif (lan == 2) and (style == 4):
            return config.ai_style_Max_en

    def free_try(user_id, get_time):
        if (func.sub_check(get_time) == False) and (db.get_free(user_id) > 0):
            db.set_free(user_id, (db.get_free(user_id)-1))
            return True
        elif func.sub_check(get_time) != False:
            return True
        else:
            return False

    def get_response(messages, temperature, top_p, frequency_penalty, presence_penalty):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty)
        return completion.choices[0].message.content

    def to_list(l):
        result = [x.strip() for x in l.split('{|}')]
        return result

    def context_append(user_id, message):
        text = str(db.context_check(user_id))
        text = text + str(message) + "{|}"
        db.context_append(user_id, text)

    def to_context(user_id, style, text):
        string = db.context_check(user_id)
        list = to_list(str(string))
        messages = [{"role": "system", "content": lang_check(user_id, style)}]
        for i in range(1, len(list)):
            if i%2!=0:
                messages.append({"role": "user", "content": list[i]})
            elif i%2==0:
                messages.append({"role": "assistant", "content": list[i]})
        messages.append({"role": "user", "content": text})
        db.context_append(user_id, text+"{|}")
        return messages

    @dp.message_handler(commands='start')
    async def cmd_start(message: types.Message):
        if message.chat.type == "private":
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id)
        await bot.send_message(chat_id=message.chat.id,text=config.start_text,reply_markup=mk.MainMenu)

    @dp.callback_query_handler(text_contains="Mary")
    async def check(callback: types.CallbackQuery):
        db.set_style(callback.from_user.id, 1)
        await bot.send_message(callback.from_user.id, config.Mary_Hello)

    @dp.callback_query_handler(text_contains="Clover")
    async def check(callback: types.CallbackQuery):
        db.set_style(callback.from_user.id, 2)
        await bot.send_message(callback.from_user.id,  config.Clover_Hello)

    @dp.callback_query_handler(text_contains="Nat-Chan")
    async def check(callback: types.CallbackQuery):
        db.set_style(callback.from_user.id, 3)
        await bot.send_message(callback.from_user.id, config.Nat_Chan_Hello)

    @dp.callback_query_handler(text_contains="Max")
    async def check(callback: types.CallbackQuery):
        db.set_style(callback.from_user.id, 4)
        await bot.send_message(callback.from_user.id,  config.Max_Hello)

    @dp.callback_query_handler(text_contains="RU")
    async def check(callback: types.CallbackQuery):
        db.set_language(callback.from_user.id, 1)
        await bot.send_message(callback.from_user.id,  "Вы выбрали русский язык")

    @dp.callback_query_handler(text_contains="EN")
    async def check(callback: types.CallbackQuery):
        db.set_language(callback.from_user.id, 2)
        await bot.send_message(callback.from_user.id,  "You have chosen English")

    @dp.message_handler(commands='pay')
    async def cmd_pay(message: types.Message):
        comment = str(message.from_user.id) + "_" + str(random.randint(1000, 9999))
        bill = p2p.bill(amount=config.price, lifetime=15, comment=comment)
        db.add_check(message.from_user.id, bill.bill_id)
        await bot.send_message(message.from_user.id, "Вам нужно оформить подписку сроком на 30 дней по цене 290 рублей", reply_markup=mk.buy_menu(url=bill.pay_url, bill=bill.bill_id))

    @dp.callback_query_handler(text_contains="pay")
    async def check(callback: types.CallbackQuery):
        comment = str(callback.from_user.id) + "_" + str(random.randint(1000, 9999))
        bill = p2p.bill(amount=config.price, lifetime=15, comment=comment)
        db.add_check(callback.from_user.id, bill.bill_id)
        await bot.send_message(callback.from_user.id, "Вам нужно оформить подписку сроком на 30 дней по цене 290 рублей. Для этого пройдите по ссылке на оплату, а затем ОБЯЗАТЕЛЬНО проверьте оплату.",
                               reply_markup=mk.buy_menu(url=bill.pay_url, bill=bill.bill_id))

    @dp.callback_query_handler(text_contains="check_")
    async def check(callback: types.CallbackQuery):
        bill = str(callback.data[6:])
        info = db.get_check(bill)
        if info != False:
            if str(p2p.check(bill_id=bill).status)=="PAID":
                time_sub = int(time.time()) + func.to_seconds(30)
                db.set_time_sub(callback.from_user.id, time_sub)
                db.delete_check(bill)
                await bot.send_message(callback.from_user.id, "Поздравляю, вы приобрели подписку! Приятного пользования.")
            else:
                await bot.send_message(callback.from_user.id, "Вы не оплатили подписку!", reply_markup=mk.buy_menu(False, bill=bill))
        else:
            await bot.send_message(callback.from_user.id, "Счет не найден")

    @dp.message_handler(content_types=['text'])
    async def handle_text(message: types.Message):
        response = None
        chat_id = message.chat.id
        style = db.get_style(chat_id)
        if message.text == "Выбрать язык":
            await bot.send_message(chat_id=message.chat.id,text="Выберите язык.",reply_markup=mk.lanMenu)
        elif message.text == "Очистить контекст":
            db.context_append(chat_id, "")
            await bot.send_message(chat_id=message.chat.id,text="Контекст очищен.",reply_markup=mk.MainMenu)
        elif message.text == "Помощь":
            await bot.send_message(chat_id=message.chat.id, text=config.help_text,)
        elif message.text == "Моя подписка":
            if func.sub_check(db.get_time_sub(message.from_user.id)) != False:
                await bot.send_message(chat_id=message.chat.id, text=("Ваша подписка составляет: "+ str(func.sub_check(db.get_time_sub(message.from_user.id)))),)
            else:
                await bot.send_message(chat_id=message.chat.id, text="У вас нет действующей подписки", reply_markup=mk.topUpMenu)
        elif message.text == "Изменить стиль":
            await bot.send_message(chat_id=message.chat.id, text = config.style_set_text, reply_markup=mk.styleMenu)
        else:
            if free_try(chat_id, db.get_time_sub(message.from_user.id))==False:
                await bot.send_message(chat_id=message.chat.id, text="У вас нет действующей подписки", reply_markup=mk.topUpMenu)
            else:
                if style == 1:
                    context_append(chat_id, message.text)
                    messages = to_context(chat_id, style, message.text)
                    response = get_response(messages, 0.9, 1.0, 0.0, 0.6)
                    context_append(chat_id, response)
                    await bot.send_message(chat_id=chat_id, text=response,reply_markup=mk.MainMenu)
                elif style == 2:
                    messages = to_context(chat_id, style, message.text)
                    response = get_response(messages, 0.5, 1.0, 0.0, 0.0)
                    db.context_append(chat_id, response + "{|}")
                    await bot.send_message(chat_id=chat_id, text=response,reply_markup=mk.MainMenu )
                elif style == 3:
                    messages = to_context(chat_id, style, message.text)
                    response = get_response(messages, 0.5, 1.0, 0.5, 0.0)
                    db.context_append(chat_id, response + "{|}")
                    await bot.send_message(chat_id=chat_id, text=response,reply_markup=mk.MainMenu )
                elif style == 4:
                    messages = to_context(chat_id, style, message.text)
                    response = get_response(messages, 0.5, 1.0, 0.5, 0.0)
                    db.context_append(chat_id, response + "{|}")
                    await bot.send_message(chat_id=chat_id, text=response,reply_markup=mk.MainMenu )

    executor.start_polling(dp, skip_updates=False)

def run_bot():
    while True:
        try:
            start_bot()
        except openai.error.APIConnectionError:
            print('Ошибка соединения с API OpenAI. Бот будет перезапущен через 2 секунды.')
            time.sleep(2)
            continue
        except exceptions.NetworkError as e:
            print("Ошибка соединения с серверами Телеграмм. Бот будет перезапущен через 2 секунды.")
            time.sleep(2)
            continue


if __name__ == "__main__":
    run_bot()