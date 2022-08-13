import telebot
import config
import datetime
import json
import traceback
from utils import serialize_table, get_back_keyboard, getHTML, get_defi_keyboard
from backend import get_user_transactions, get_user_balances, set_user_address, get_user_address



from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(level=logging.INFO)

from config import TOKEN



import logging




from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


bot = telebot.TeleBot('5458976355:AAFjGkLkgV5QsBI7LEQOPeqKQZmsmUa70oE')
print(bot)

@dp.message_handler(commands='start')
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Начать', callback_data='home'
        )
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Помощь', callback_data='home'
        )
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton(
            'Сделано Егором и Даней', callback_data='a'
        )
    )
    bot.send_message(
        message.chat.id,
        "Привествуем!\n" +
        "Чтобы начать, пропишите /home\n" +
        "Если нужна помощь, пропишите /help",
        reply_markup=keyboard
    )

@dp.message_handler(commands='help')
def help_command(message):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.add(
       telebot.types.InlineKeyboardButton(
           'Наши контакты', url='telegram.me/Glob1s'
       )
   )
   bot.send_message(
       message.chat.id,
       '1) Что бы настроить кошелёк, пропишите /home \n' +
       '2) Нажмите на то, что вас интересует\n',
       reply_markup=keyboard
   )

@dp.message_handler(commands='home')
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
      telebot.types.InlineKeyboardButton('Баласнс', callback_data='bal')
    )
    keyboard.row(
    telebot.types.InlineKeyboardButton('Последние трансакции', callback_data='trans'),
    telebot.types.InlineKeyboardButton('Управление ботом', callback_data='defi')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Зарегестрировать/обновить адресс', callback_data='setAddress')
    )

    bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboard)

@dp.message_handler(content_types='text')
def set_user_address_handler(message):
    sent = bot.send_message(message.chat.id, '')

def set_address(msg):
    print(msg.from_user.id, msg.text)
    if msg.text[0:2] == '0x' and len(msg.text) == 42:
        set_user_address(msg.from_user.id, msg.text)
        bot.send_message(msg.chat.id, 'Новый адресс установлен!')
    else:
        bot.send_message(msg.chat.id, 'Неправильный адресс. Перезапустите бота и введите новый.')
    bot.register_next_step_handler(sent, set_address)


@dp.callback_query_handler(func=lambda call: True)

def callback(query):
    print(query)
    data = query.data
    if data == 'bal':
        items = get_user_balances(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        bot.send_message(
            query.message.chat.id, getHTML('balances', items),
            reply_markup=get_back_keyboard("bal"),
            parse_mode='HTML'
        )
    elif data == 'trans':
        items = get_user_transactions(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        print(getHTML('transactions', items))
        bot.send_message(
            query.message.chat.id, getHTML('transactions', items),
            reply_markup=get_back_keyboard("trans"),
            parse_mode='HTML'
        )
    elif data == 'defi':

        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        bot.send_message(
            query.message.chat.id, "Выберите платформу",
            reply_markup=get_defi_keyboard("send"),
            parse_mode='HTML'
        )

    elif data == 'setAddress':
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        set_user_address_handler(query.message)

    elif data == "home":
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        exchange_command(query.message)

    elif data == "refreshbal":
        items = get_user_balances(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        bot.send_message(
            query.message.chat.id, getHTML('balances', items),
            reply_markup=get_back_keyboard("bal"),
            parse_mode='HTML'
        )

    elif data == "refreshtrans":
        items = get_user_transactions(query)
        bot.answer_callback_query(query.id)
        bot.send_chat_action(query.message.chat.id, 'typing')
        print(getHTML('transactions', items))
        bot.send_message(
            query.message.chat.id, getHTML('transactions', items),
            reply_markup=get_back_keyboard("trans"),
            parse_mode='HTML'
        )


bot.polling(none_stop=True)
