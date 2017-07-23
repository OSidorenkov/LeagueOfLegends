# -*- coding: utf-8 -*-

import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    sent = bot.send_message(message.chat.id, "Здаров, чувак! ты кто&?")
    bot.register_next_step_handler(sent, hello)


def hello(message):
    bot.send_message(message.chat.id, 'Красава, {name}. Рад тебя видеть.'.format(name=message.text))


# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def menu(message):
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     summoner = types.KeyboardButton('Summoner')
#     history = types.InlineKeyboardButton('History')
#     kda = types.KeyboardButton('KDA')
#     online = types.InlineKeyboardButton('Online')
#     markup.add(summoner, history, kda, online)
#     bot.send_message(message.chat.id, "Выбери, что ты хочешь:", reply_markup=markup)


@bot.message_handler(commands=['summoner'])
def command_summoner(message):
    summoner = bot.send_message(message.chat.id, "Напиши имя своего чампа:")

if __name__ == '__main__':
    bot.polling(none_stop=True)
