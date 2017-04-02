#!/usr/bin/python
from telegram import Chat
from telegram.ext import CommandHandler
from telegram.ext import Filters

def setup_handler(dispatcher):
    handler = CommandHandler('whois', whois, Filters.command)
    dispatcher.add_handler(handler);

def whois(bot, update):
    if update.message.chat.type != Chat.PRIVATE:
        return
    message = "Hello {0}, I am {1}, the Telegram communication bot for VancouFur staff!".format(update.message.from_user.first_name, bot.first_name)
    bot.sendMessage(update.message.chat_id, message)        
