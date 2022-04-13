import json
import pickle
import types

import flask
import telebot
from google.auth.transport import requests

import conf, keyboards
import pandas as pd
import random
import xgboost as xgb
from flask_sqlalchemy import SQLAlchemy

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN,
                      threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет!')
    bot.send_message(message.chat.id, 'Я бот, с которым можно посревноваться в угадывании оригинальности. Поиграем?',
                     reply_markup=keyboards.keyboard_first
                     )


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Бот предлагает пользователю сыграть в игру против компьютера. Цель игры - угадать, где оригинальное предложение из стихотворения Бориса Рыжего, а где подделка.")


@bot.callback_query_handler(func=lambda call: True)
def send_welcome(call):
    if call.data == "yes":
        user_id = call.message.chat.id
        print(user_id)
        bot.send_message(chat_id=call.message.chat.id, text='Ок, тогда начинаем')
    else:
        bot.send_message(chat_id=call.message.chat.id, text='Тогда можешь почитать об авторе тут',
                         reply_markup=keyboards.keyboard_second
                         )


if __name__ == '__main__':
    bot.polling(none_stop=True)

model = pickle.load(open('model.pkl', 'rb'))

git rm
