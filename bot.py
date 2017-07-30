# -*- coding: utf-8 -*-

import telebot
import config
import sqlite3
import os
import time
from telebot import types
import lol_api

commands = {  # command description used in the "help" command
              'start': 'Get used to the bot',
              'help': 'Даст информацию о доступных командах',
              'getImage': 'A test using multi-stage messages, custom keyboard, and media sending',
              'summoner': 'Поменять имя призывателя'
}

hideBoard = types.ReplyKeyboardRemove()


def get_user(cid):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'bot.db'))
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists users
                (chat_id integer, summoner text)''')
    conn.commit()
    c.execute('SELECT summoner FROM users WHERE chat_id=?', (cid,))
    result = c.fetchall()
    if not result:
        return result
    else:
        return result[0][0]


def append_user(cid, summoner):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'bot.db'))
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?);", (cid, summoner))
    conn.commit()


def update_user(cid, summoner):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'bot.db'))
    c = conn.cursor()
    c.execute("UPDATE users SET summoner=? WHERE chat_id=?;", (summoner, cid))
    conn.commit()


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(config.bot_token)
bot.set_update_listener(listener)  # register listener


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    user = get_user(cid)
    if not user:
        bot.send_message(cid, "Рад тебя видеть чампион! Напиши свой ник, чтобы я заценил как ты тащишь катки =)")
        bot.register_next_step_handler(m, step_append_user)
    else:
        bot.send_message(cid, "Рад тебя снова видеть чампион! Я тебя знаю, ты {}".format(user))
        bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
        time.sleep(1)
        bot.send_message(cid, "Введи /help для просмотра доступных команд.")


def step_append_user(m):
    cid = m.chat.id
    name = m.text
    append_user(cid, name)
    bot.send_message(cid, "Я добавил тебя в свой блокнотик.")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    bot.send_message(cid, "Введи /help для просмотра доступных команд.")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Доступны следующие команды: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(commands=['summoner'])
def command_summoner(m):
    cid = m.chat.id
    # this is the standard reply to a normal message
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    msg = bot.reply_to(m, "Введи имя призывателя")
    bot.register_next_step_handler(msg, step_summoner)


def step_summoner(m):
    cid = m.chat.id
    name = m.text
    update_user(cid, name)
    bot.send_message(cid, "Имя призывателя изменено!")


@bot.message_handler(commands=['ranked'])
def command_ranked(m):
    cid = m.chat.id
    sumname = get_user(cid)
    # this is the standard reply to a normal message
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    bot.send_message(m.chat.id, "Твоя стата в ранкеде: " + lol_api.ranked(sumname))

# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def menu(message):
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     summoner = types.KeyboardButton('Summoner')
#     history = types.InlineKeyboardButton('History')
#     kda = types.KeyboardButton('KDA')
#     online = types.InlineKeyboardButton('Online')
#     markup.add(summoner, history, kda, online)
#     bot.send_message(message.chat.id, "Выбери, что ты хочешь:", reply_markup=markup)


# default handler for every other text
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def command_default(m):
#     bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


bot.polling(none_stop=True)
