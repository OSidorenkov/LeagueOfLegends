# -*- coding: utf-8 -*-

import telebot
import config
import time
from telebot import types
import lol_api

knownUsers = {}  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
              'start': 'Get used to the bot',
              'help': 'Gives you information about the available commands',
              'sendLongText': 'A test using the \'send_chat_action\' command',
              'getImage': 'A test using multi-stage messages, custom keyboard, and media sending'
}


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


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


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Рад тебя видеть чампион! Светани свой ник, чтобы я заценил как ты тащишь катки =)")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")


@bot.message_handler(func=lambda message: message.text == "Привет")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Ку-ку епта!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    cid = m.chat.id
    sumname = m.text
    # this is the standard reply to a normal message
    lol_api.summoner(sumname)
    knownUsers[cid] = sumname
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    bot.send_message(m.chat.id, "Чекнул.. Конечно, я ожидал большего")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(1)
    bot.send_message(m.chat.id, "Твой левел = " + lol_api.summoner(sumname))

    # bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


@bot.message_handler(commands=['ranked'])
def command_ranked(m):
    cid = m.chat.id
    sumname = knownUsers[cid]
    print(sumname)
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


# @bot.message_handler(commands=['summoner'])
# def command_summoner(message):
#     summoner = bot.send_message(message.chat.id, "Напиши имя своего чампа:")
#     bot.register_next_step_handler(summoner, local)


if __name__ == '__main__':
    bot.polling(none_stop=True)
