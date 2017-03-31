#!/usr/bin/python
from telegram.ext import CommandHandler

def setup_handler(dispatcher):
    handler = CommandHandler('whois', whois)
    dispatcher.add_handler(handler);

def whois(bot, update):
    message = "Hello {0}, I am {1}, the Telegram communication bot for VancouFur staff!".format(update.message.from_user.first_name, bot.first_name)
    bot.sendMessage(update.message.chat_id, message)        
